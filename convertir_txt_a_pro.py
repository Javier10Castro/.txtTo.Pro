from pathlib import Path
import uuid
import re

BASE = Path(__file__).resolve().parent
INPUT_DIR = BASE / "Canciones"
OUTPUT_DIR = BASE / "SalidaPro"
TEMPLATE = BASE / "plantilla.pro"


def read_varint(b, i):
    x = 0
    shift = 0
    while True:
        if i >= len(b):
            raise ValueError("Varint incompleto")
        c = b[i]
        i += 1
        x |= (c & 0x7F) << shift
        if c < 128:
            return x, i
        shift += 7


def parse_fields(b):
    out = []
    i = 0
    while i < len(b):
        start = i
        tag, i = read_varint(b, i)
        fn, wt = tag >> 3, tag & 7
        if wt == 0:
            v, i = read_varint(b, i)
        elif wt == 1:
            v = b[i:i+8]
            i += 8
        elif wt == 2:
            n, i = read_varint(b, i)
            v = b[i:i+n]
            i += n
        elif wt == 5:
            v = b[i:i+4]
            i += 4
        else:
            raise ValueError(f"Wire type no soportado: {wt}")
        out.append((fn, wt, v, start, i))
    return out


def enc_varint(x):
    out = bytearray()
    while x >= 128:
        out.append((x & 0x7F) | 0x80)
        x >>= 7
    out.append(x)
    return bytes(out)


def enc_field(fn, wt, value):
    out = enc_varint((fn << 3) | wt)
    if wt == 0:
        return out + enc_varint(value)
    if wt == 1:
        return out + value
    if wt == 2:
        return out + enc_varint(len(value)) + value
    if wt == 5:
        return out + value
    raise ValueError(f"Wire type no soportado: {wt}")


def serialize_fields(items):
    return b"".join(enc_field(fn, wt, value) for fn, wt, value in items)


def transform_first(data, field_number, transform):
    done = False
    result = []
    for fn, wt, value, _, _ in parse_fields(data):
        if fn == field_number and not done:
            value = transform(value)
            done = True
        result.append((fn, wt, value))
    return serialize_fields(result)


def transform_all(data, field_number, transform):
    result = []
    for fn, wt, value, _, _ in parse_fields(data):
        if fn == field_number:
            value = transform(value)
        result.append((fn, wt, value))
    return serialize_fields(result)


def uuid_message(value):
    return enc_field(1, 2, value.encode("ascii"))


def rtf_escape(text):
    out = []
    for ch in text:
        code = ord(ch)
        if ch == "\\":
            out.append(r"\\")
        elif ch == "{":
            out.append(r"\{")
        elif ch == "}":
            out.append(r"\}")
        elif code < 128:
            out.append(ch)
        else:
            signed = code if code < 32768 else code - 65536
            out.append(rf"\u{signed} ?")
    return "".join(out)


def build_rtf(lines, template_rtf):
    t = template_rtf.decode("cp1252", errors="replace")
    marker = (
        r"\pard\li0\fi0\ri0\qc\sb0\sa0\sl240\slmult1\slleading0"
        r"\f0\b0\i0\ul0\strike0\fs100\expnd0\expndtw0\cf1"
        r"\strokewidth0\strokec1\nosupersub\ulc0\highlight2\cb2 "
    )
    first_pard = t.find(r"\pard")
    if first_pard < 0:
        raise ValueError("No se encontró el encabezado RTF de la plantilla.")

    prefix = t[:first_pard]
    body = [marker + rtf_escape(line) + r"\par" for line in lines]
    return (prefix + "".join(body) + "}0").encode("cp1252", errors="replace")


def split_txt(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    blocks = re.split(r"\n[ \t]*\n(?:[ \t]*\n)*", text)

    slides = []
    for block in blocks:
        lines = [line.rstrip() for line in block.split("\n")]

        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        if lines:
            # Compatibilidad: si algún archivo todavía tiene // de una
            # conversión anterior, se ignora esa línea.
            lines = [line for line in lines if line.strip() != "//"]
            if lines:
                slides.append(lines)

    return slides


def extract_template_parts(template):
    top = parse_fields(template)
    cue_values = [v for fn, wt, v, _, _ in top if fn == 13]
    if not cue_values:
        raise ValueError("La plantilla no contiene ningún cue (campo 13).")

    template_cue = cue_values[0]

    cue_action = [v for fn, wt, v, _, _ in parse_fields(template_cue) if fn == 10][0]
    slide_type = [v for fn, wt, v, _, _ in parse_fields(cue_action) if fn == 23][0]
    presentation_slide = [v for fn, wt, v, _, _ in parse_fields(slide_type) if fn == 2][0]
    base_slide = [v for fn, wt, v, _, _ in parse_fields(presentation_slide) if fn == 1][0]
    element = [v for fn, wt, v, _, _ in parse_fields(base_slide) if fn == 1][0]
    graphics_element = [v for fn, wt, v, _, _ in parse_fields(element) if fn == 1][0]
    text_message = [v for fn, wt, v, _, _ in parse_fields(graphics_element) if fn == 13][0]
    template_rtf = [v for fn, wt, v, _, _ in parse_fields(text_message) if fn == 5][0]

    return top, template_cue, template_rtf


def make_cue(template_cue, lines, template_rtf):
    cue_id = str(uuid.uuid4())
    action_id = str(uuid.uuid4())
    slide_id = str(uuid.uuid4())
    element_id = str(uuid.uuid4())
    new_rtf = build_rtf(lines, template_rtf)

    def mod_graphics_element(data):
        data = transform_first(data, 1, lambda _: uuid_message(element_id))
        data = transform_first(
            data,
            13,
            lambda text: transform_first(text, 5, lambda _: new_rtf)
        )
        return data

    def mod_element(data):
        return transform_first(data, 1, mod_graphics_element)

    def mod_base_slide(data):
        data = transform_first(data, 1, mod_element)
        data = transform_first(data, 7, lambda _: uuid_message(slide_id))
        return data

    def mod_presentation_slide(data):
        return transform_first(data, 1, mod_base_slide)

    def mod_slide_type(data):
        return transform_first(data, 2, mod_presentation_slide)

    def mod_action(data):
        data = transform_first(data, 1, lambda _: uuid_message(action_id))
        data = transform_first(data, 23, mod_slide_type)
        return data

    cue = transform_first(template_cue, 1, lambda _: uuid_message(cue_id))
    cue = transform_all(cue, 10, mod_action)
    return cue, cue_id


def build_pro(template, title, slides):
    top, template_cue, template_rtf = extract_template_parts(template)
    presentation_uuid = str(uuid.uuid4())

    cues = []
    cue_ids = []
    for slide in slides:
        cue, cue_id = make_cue(template_cue, slide, template_rtf)
        cues.append(cue)
        cue_ids.append(cue_id)

    original_group_values = [v for fn, wt, v, _, _ in top if fn == 12]
    original_group = original_group_values[0] if original_group_values else None

    output = []

    for fn, wt, value, _, _ in top:
        if fn == 2:
            value = uuid_message(presentation_uuid)

        elif fn == 3:
            value = title.encode("utf-8")

        elif fn == 12 and original_group is not None:
            group_fields = [
                (gfn, gwt, gv)
                for gfn, gwt, gv, _, _ in parse_fields(original_group)
                if gfn != 2
            ]
            group_fields.extend((2, 2, uuid_message(cid)) for cid in cue_ids)
            value = serialize_fields(group_fields)

        elif fn == 13:
            continue

        output.append((fn, wt, value))

    output.extend((13, 2, cue) for cue in cues)
    return serialize_fields(output)


def main():
    print("========================================")
    print(" CONVERSOR TXT -> PROPRESENTER .PRO")
    print("========================================")
    print()

    if not TEMPLATE.exists():
        print(f"[ERROR] No existe la plantilla:")
        print(f"        {TEMPLATE}")
        print()
        print("Copia tu archivo .pro de referencia a esa ruta")
        print("y renómbralo exactamente como: plantilla.pro")
        input("Presiona ENTER para salir...")
        return

    if not INPUT_DIR.exists():
        print(f"[ERROR] No existe la carpeta: {INPUT_DIR}")
        input("Presiona ENTER para salir...")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    try:
        template = TEMPLATE.read_bytes()
        extract_template_parts(template)
    except Exception as e:
        print(f"[ERROR] La plantilla .pro no pudo analizarse: {e}")
        input("Presiona ENTER para salir...")
        return

    files = sorted(INPUT_DIR.glob("*.txt"))
    if not files:
        print(f"[AVISO] No hay archivos .txt en {INPUT_DIR}")
        input("Presiona ENTER para salir...")
        return

    ok = 0
    errors = 0

    for txt_file in files:
        try:
            try:
                text = txt_file.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                text = txt_file.read_text(encoding="cp1252")

            slides = split_txt(text)

            if not slides:
                print(f"[OMITIDO] {txt_file.name}: no contiene texto.")
                continue

            result = build_pro(template, txt_file.stem, slides)
            out_file = OUTPUT_DIR / f"{txt_file.stem}.pro"
            out_file.write_bytes(result)

            print(f"[OK] {txt_file.name} -> {out_file.name} ({len(slides)} slides)")
            ok += 1

        except Exception as e:
            print(f"[ERROR] {txt_file.name}: {e}")
            errors += 1

    print()
    print("========================================")
    print(f" Terminados: {ok}")
    print(f" Errores:    {errors}")
    print(f" Salida:     {OUTPUT_DIR}")
    print("========================================")
    input("Presiona ENTER para salir...")


if __name__ == "__main__":
    main()
