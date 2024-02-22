import dbf
import re
import subprocess
import tempfile
import typer
import shutil
from pathlib import Path
from typing import List
from pyfoxpro.foxpro import replacement_table, properties_to_remove


app = typer.Typer()


@app.command()
def beautify(file: str, vfp6: bool = False):
    file_path = Path(file)

    if not file_path.exists() \
            or file_path.is_dir() \
            or not (file_path.suffix.lower() == ".scx"
                    or file_path.suffix.lower() == ".sc2"
                    or file_path.suffix.lower() == ".mnx"
                    or file_path.suffix.lower() == ".mn2"
                    or file_path.suffix.lower() == ".vc2"
                    or file_path.suffix.lower() == ".vcx"
                    or file_path.suffix.lower() == ".fr2"
                    or file_path.suffix.lower() == ".frx"
                    or file_path.suffix.lower() == ".prg"):
        return

    if file_path.suffix.lower() == ".prg":
        with file_path.open("r", newline="\r\n") as f:
            beautified_code_lines = beautify_code(f.read(), False)

        with file_path.open("w", newline="\r\n") as f:
            f.write("\n".join(beautified_code_lines))

        return

    if file_path.suffix.lower() == ".mn2":
        file_path = file_path.with_suffix(".mnx")

    if file_path.suffix.lower() == ".mnx":
        form_memo = file_path.with_suffix(".mnt")
        temp_form_memo = form_memo.rename(form_memo.with_suffix(".fpt"))

        table = dbf.Table(filename=str(file_path))

        table.open(dbf.READ_WRITE)
        try:
            for record in table:
                if record.command:
                    beatified_code = beautify_code(record.command, True)
                    dbf.write(record, command="\r\n".join(beatified_code))
                if record.procedure:
                    beatified_code = beautify_code(record.procedure, True)
                    dbf.write(record, procedure="\r\n".join(beatified_code))
                if record.skipfor:
                    beatified_code = beautify_code(record.skipfor, True)
                    dbf.write(record, skipfor="\r\n".join(beatified_code))
        finally:
            table.close()
            temp_form_memo.rename(form_memo)

        if vfp6:
            file_path_backup = file_path.with_name(file_path.name + "_backup")
            form_memo_backup = form_memo.with_name(form_memo.name + "_backup")

            shutil.copy2(str(file_path), str(file_path_backup))
            shutil.copy2(str(form_memo), str(form_memo_backup))

            foxpro_modify_menu_file: Path = Path(tempfile.gettempdir() + "\\modify_menu.prg")
            foxpro_modify_menu_file_fxp: Path = foxpro_modify_menu_file.with_suffix(".fxp")
            with foxpro_modify_menu_file.open(mode="w") as f:
                f.write(f"MODIFY MENU {str(file_path)} NOWAIT\n")

            subprocess.run(["vfp9", "-c", str(foxpro_modify_menu_file)])

            foxpro_modify_menu_file.unlink()
            foxpro_modify_menu_file_fxp.unlink()

        subprocess.run(["foxbin2prg", str(file_path), "BIN2PRG"])

        if vfp6:
            file_path.unlink()
            form_memo.unlink()

            shutil.copy2(str(file_path_backup), str(file_path))
            shutil.copy2(str(form_memo_backup), str(form_memo))

            file_path_backup.unlink()
            form_memo_backup.unlink()

        return

    if file_path.suffix.lower() == ".fr2":
        file_path = file_path.with_suffix(".frx")

    if file_path.suffix.lower() == ".frx":
        form_memo = file_path.with_suffix(".frt")
        temp_form_memo = form_memo.rename(form_memo.with_suffix(".fpt"))

        table = dbf.Table(filename=str(file_path))

        table.open(dbf.READ_WRITE)
        try:
            for record in table:
                if record.name in properties_to_remove:
                    properties_splited: str = record.expr.splitlines(keepends=True)
                    clean_properties: List[str] = []

                    for prop in properties_splited:
                        good_prop = True

                        if "ControlSource" in prop or "DynamicBackColor" in prop or "DynamicForeColor" in prop:
                            if '= "' in prop:
                                content_regex = re.compile(r'".*"')
                            elif "= '" in prop:
                                content_regex = re.compile(r"'.*'")
                            else:
                                content_regex = re.compile(r"\[.*]")

                            search_result = content_regex.search(prop)

                            corrected_prop = beautify_code(search_result.group(0)[1:-1], False)[0]

                            if '"' in corrected_prop and "'" in corrected_prop:
                                replacement_prop = f"[{corrected_prop}]"
                            elif '"' in corrected_prop:
                                replacement_prop = f"'{corrected_prop}'"
                            else:
                                replacement_prop = f'"{corrected_prop}"'

                            prop = content_regex.sub(replacement_prop, prop)

                        for prop_to_remove in properties_to_remove[record.name]:
                            if prop_to_remove.search(prop):
                                good_prop = False
                                break

                        if good_prop:
                            if "= (" in prop:
                                corrected_prop = beautify_code(re.search(r'\(.*\)', prop).group(0)[1:-1], False)[0]
                                prop = re.sub(r'\(.*\)', f'({corrected_prop.replace("\\", "\\\\")})', prop)

                            clean_properties.append(prop)

                    dbf.write(record, expr="".join(clean_properties))
                if record.objtype != 1 and record.objtype != 25 and record.objtype != 26 and record.expr:
                    beatified_code = beautify_code(record.expr, True, True)
                    dbf.write(record, expr="\r\n".join(beatified_code))
                if record.objtype != 1 and record.tag:
                    beatified_code = beautify_code(record.tag, True)
                    dbf.write(record, tag="\r\n".join(beatified_code))
                if record.supexpr:
                    beatified_code = beautify_code(record.supexpr, True)
                    dbf.write(record, supexpr="\r\n".join(beatified_code))
        finally:
            table.close()
            temp_form_memo.rename(form_memo)

        foxpro_compile_command_file: Path = Path(tempfile.gettempdir() + "\\compile_file.prg")
        foxpro_compile_command_file_fxp: Path = foxpro_compile_command_file.with_suffix(".fxp")
        with foxpro_compile_command_file.open(mode="w") as f:
            f.write(f"COMPILE REPORT {str(file_path)}\nQUIT\n")

        subprocess.run(["vfp9", "-c", str(foxpro_compile_command_file)])

        foxpro_compile_command_file.unlink()
        foxpro_compile_command_file_fxp.unlink()

        subprocess.run(["foxbin2prg", str(file_path), "BIN2PRG"])

        return

    if file_path.suffix.lower() == ".sc2":
        file_path = file_path.with_suffix(".scx")
    if file_path.suffix.lower() == ".vc2":
        file_path = file_path.with_suffix(".vcx")

    suffix = ".sct"
    object_type = "FORM"
    if file_path.suffix.lower() == ".vcx":
        suffix = ".vct"
        object_type = "CLASSLIB"

    form_memo: Path = file_path.with_suffix(suffix)
    temp_form_memo = form_memo.rename(form_memo.with_suffix(".fpt"))

    table = dbf.Table(
        filename=str(file_path)
    )

    table.open(dbf.READ_WRITE)

    for record in table:
        if record["class"] in properties_to_remove:
            properties_splited: str = record.properties.splitlines(keepends=True)
            clean_properties: List[str] = []

            for prop in properties_splited:
                good_prop = True

                if "ControlSource" in prop or "DynamicBackColor" in prop or "DynamicForeColor" in prop:
                    if '= "' in prop:
                        content_regex = re.compile(r'".*"')
                    elif "= '" in prop:
                        content_regex = re.compile(r"'.*'")
                    else:
                        content_regex = re.compile(r"\[.*]")

                    search_result = content_regex.search(prop)

                    corrected_prop = beautify_code(search_result.group(0)[1:-1], False)[0]

                    if '"' in corrected_prop and "'" in corrected_prop:
                        replacement_prop = f"[{corrected_prop}]"
                    elif '"' in corrected_prop:
                        replacement_prop = f"'{corrected_prop}'"
                    else:
                        replacement_prop = f'"{corrected_prop}"'

                    prop = content_regex.sub(replacement_prop, prop)

                for prop_to_remove in properties_to_remove[record["class"]]:
                    if prop_to_remove.search(prop):
                        good_prop = False
                        break

                if good_prop:
                    if "= (" in prop:
                        corrected_prop = beautify_code(re.search(r'\(.*\)', prop).group(0)[1:-1], False)[0]
                        prop = re.sub(r'\(.*\)', f'({corrected_prop.replace("\\", "\\\\")})', prop)

                    clean_properties.append(prop)

            dbf.write(record, properties="".join(clean_properties))

        if record.methods:
            beatified_code = beautify_code(record.methods, True)
            dbf.write(record, methods="\r\n".join(beatified_code))

    table.close()

    temp_form_memo.rename(form_memo)

    foxpro_compile_command_file: Path = Path(tempfile.gettempdir() + "\\compile_file.prg")
    foxpro_compile_command_file_fxp: Path = foxpro_compile_command_file.with_suffix(".fxp")
    with foxpro_compile_command_file.open(mode="w") as f:
        f.write(f"COMPILE {object_type} {str(file_path)}\nQUIT\n")

    subprocess.run(["vfp9", "-c", str(foxpro_compile_command_file)])

    foxpro_compile_command_file.unlink()
    foxpro_compile_command_file_fxp.unlink()

    subprocess.run(["foxbin2prg", str(file_path), "BIN2PRG"])


def convert_iif_isnull_to_nvl(match) -> str:
    return f"NVL({match.group(1)}, {match.group(2)})"


def beautify_code(code: str, is_form: bool, is_report_expr: bool = False) -> List[str]:
    lines: List[str] = code.split(sep="\r\n") if not is_report_expr else [code]
    corrected_lines: List[str] = []
    indentation_level = 0

    operator_to_insert = ""

    continuation_line = False

    binary_operator_on_two_lines = False

    for line in lines:
        line_stripped: str = line.strip()

        if line_stripped.startswith("PROCEDURE") and is_form:
            corrected_lines.append(line_stripped)
            continue

        if not line_stripped:
            corrected_lines.append(line_stripped)
            continue

        if line_stripped.startswith("&&"):
            line_stripped = line_stripped.replace("&&", "*", 1)

        if line_stripped.startswith("*"):
            corrected_lines.append("\t" * indentation_level + line_stripped)
            continue

        if line_stripped.upper().startswith("ELSE"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDIF"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDSCAN"):
            indentation_level -= 1
        if line_stripped.upper().startswith("CASE"):
            indentation_level -= 1
        if line_stripped.upper().startswith("OTHER"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDCASE"):
            indentation_level -= 2
        if line_stripped.upper().startswith("ENDFOR"):
            indentation_level -= 1
        if line_stripped.upper().startswith("NEXT"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDDO"):
            indentation_level -= 1
        if line_stripped.upper().startswith("CATCH"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDTRY"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDWITH"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDFUNC"):
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDPROC") and not is_form:
            indentation_level -= 1
        if line_stripped.upper().startswith("ENDDEFINE"):
            indentation_level -= 1

        comment_start = line_stripped.find("&&")
        comment = ""
        if comment_start != -1:
            comment = re.sub(r"&&\s*", "&& ", line_stripped[comment_start:])
            line_stripped = line_stripped[:comment_start].rstrip()

        matches = [match for match in re.split(r"('[^']*')|('[^']*$)|(\"[^\"]*\")|(\"[^\"]*$)", line_stripped)
                   if match is not None]

        corrected_line = ""
        for i, match in enumerate(matches):
            comment_match = False
            match_raw = match

            if not is_report_expr and match_raw.startswith('"'):
                if match_raw.find("'") == -1:
                    match_raw = match_raw.replace('"', "'")
                comment_match = True
            if match.startswith("'") or match.startswith('"'):
                comment_match = True

            if comment_match:
                comment_content = match_raw[1:-1]
                if not is_report_expr and comment_content.isspace() and len(comment_content) > 1:
                    match_raw = f"SPACE({len(comment_content)})"
                corrected_line = corrected_line + match_raw
                continue

            for replacement in replacement_table:
                match_raw = replacement[0].sub(replacement[1], match_raw)

            match_raw = re.sub(r"\s*=\s*", " = ", match_raw)
            match_raw = re.sub(r"^\s*=\s*", "= ", match_raw)
            match_raw = re.sub(r"\s*<\s*", " < ", match_raw)
            match_raw = re.sub(r"^\s*<\s*", "< ", match_raw)
            match_raw = re.sub(r"\s*>\s*", " > ", match_raw)
            match_raw = re.sub(r"^\s*>\s*", "> ", match_raw)
            match_raw = re.sub(r"\s*=\s*=\s*", " == ", match_raw)
            match_raw = re.sub(r"^\s*=\s*=\s*", "== ", match_raw)
            match_raw = re.sub(r"\s*<\s*=\s*", " <= ", match_raw)
            match_raw = re.sub(r"^\s*<\s*=\s*", "<= ", match_raw)
            match_raw = re.sub(r"\s*>\s*=\s*", " >= ", match_raw)
            match_raw = re.sub(r"^\s*>\s*=\s*", ">= ", match_raw)
            match_raw = re.sub(r"\s*=\s*>\s*", " >= ", match_raw)
            match_raw = re.sub(r"^\s*=\s*>\s*", ">= ", match_raw)
            match_raw = re.sub(r"\s*<\s*>\s*", " <> ", match_raw)
            match_raw = re.sub(r"^\s*<\s*>\s*", "<> ", match_raw)
            match_raw = re.sub(r"\s*!\s*=\s*", " <> ", match_raw)
            match_raw = re.sub(r"^\s*!\s*=\s*", "<> ", match_raw)
            match_raw = re.sub(r"\s*#\s*", " <> ", match_raw)
            match_raw = re.sub(r"^\s*#\s*", "<> ", match_raw)

            match_raw = re.sub(r"(?<=[\w)\]'\"])(?<!WITH)(?<!STEP)(?<!SKIP)\s*\+\s*", " + ", match_raw)
            match_raw = re.sub(r"^\s*\+\s*", ("+ " if i == 0 else " + ") if not continuation_line or not (
                        not binary_operator_on_two_lines and i == 0) else "+", match_raw)
            match_raw = re.sub(r"(?<=[\w)\]'\"])(?<!WITH)(?<!STEP)(?<!SKIP)\s*-\s*", " - ", match_raw)
            match_raw = re.sub(r"^\s*-\s*", ("- " if i == 0 else " - ") if not continuation_line or not (
                        not binary_operator_on_two_lines and i == 0) else "-", match_raw)
            if "LIKE" not in match_raw:
                match_raw = re.sub(r"\s*\*\s*", " * ", match_raw)
                match_raw = re.sub(r"^\s*\*\s*", ("* " if i == 0 else " * ") if not continuation_line or not (
                            not binary_operator_on_two_lines and i == 0) else "*", match_raw)
                match_raw = re.sub(r"\s*\*\s*\*\s*", " ** ", match_raw)
                match_raw = re.sub(r"^\s*\*\s*\*\s*", ("** " if i == 0 else " ** ") if not continuation_line or not (
                            not binary_operator_on_two_lines and i == 0) else "**", match_raw)
            match_raw = re.sub(r"\s*/\s*", " / ", match_raw)
            match_raw = re.sub(r"^\s*/\s*", ("/ " if i == 0 else " / ") if not continuation_line or not (
                        not binary_operator_on_two_lines and i == 0) else "/", match_raw)
            match_raw = re.sub(r"\s*,\s*", ", ", match_raw)
            match_raw = re.sub(r"\s*;", " ;", match_raw)
            match_raw = re.sub(r"\(\s+", "(", match_raw)
            match_raw = re.sub(r"\s+\)", ")", match_raw)
            match_raw = re.sub(r"\s+", " ", match_raw)
            match_raw = re.sub(r"(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2})",
                               lambda match: f"{match.group(1)}-{match.group(2)}-{match.group(3)}", match_raw)
            match_raw = re.sub(r"(\d{2})\s*-\s*(\d{2})\s*-\s*(\d{4})",
                               lambda match: f"{match.group(1)}-{match.group(2)}-{match.group(3)}", match_raw)

            corrected_line = corrected_line + match_raw

        corrected_line = operator_to_insert + re.sub(r"IIF\(ISNULL\((?P<cond>.+)\), (.+), (?P=cond)\)",
                                                     convert_iif_isnull_to_nvl,
                                                     corrected_line)
        operator_to_insert = ""

        if corrected_line.endswith(" + ;"):
            corrected_line = corrected_line.replace(" + ;", " ;")
            operator_to_insert = "+ "
        if corrected_line.endswith(" - ;"):
            corrected_line = corrected_line.replace(" - ;", " ;")
            operator_to_insert = "- "
        if corrected_line.endswith(" * ;"):
            corrected_line = corrected_line.replace(" * ;", " ;")
            operator_to_insert = "* "
        if corrected_line.endswith(" / ;"):
            corrected_line = corrected_line.replace(" / ;", " ;")
            operator_to_insert = "/ "
        if corrected_line.endswith(" AND ;"):
            corrected_line = corrected_line.replace(" AND ;", " ;")
            operator_to_insert = "AND "
        if corrected_line.endswith(" OR ;"):
            corrected_line = corrected_line.replace(" OR ;", " ;")
            operator_to_insert = "OR "

        line_stripped = corrected_line
        corrected_line = "\t" * indentation_level + corrected_line

        if line_stripped.startswith("IF"):
            indentation_level += 1
        if line_stripped.startswith("ELSE"):
            indentation_level += 1
        if line_stripped.startswith("SCAN"):
            indentation_level += 1
        if line_stripped.startswith("DO CASE"):
            indentation_level += 2
        if line_stripped.startswith("CASE"):
            indentation_level += 1
        if line_stripped.startswith("OTHER"):
            indentation_level += 1
        if line_stripped.startswith("DO WHILE"):
            indentation_level += 1
        if line_stripped.startswith("FOR EACH"):
            indentation_level += 1
        if line_stripped.endswith(";") and not continuation_line:
            indentation_level += 1
            continuation_line = True
        if not line_stripped.endswith(";") and continuation_line:
            indentation_level -= 1
            continuation_line = False
        if re.search(r"^FOR .+ TO", line_stripped):
            indentation_level += 1
        if line_stripped.startswith("TRY"):
            indentation_level += 1
        if line_stripped.startswith("CATCH"):
            indentation_level += 1
        if line_stripped.startswith("WITH"):
            indentation_level += 1
        if line_stripped.startswith("FUNCTION"):
            indentation_level += 1
        if line_stripped.startswith("PROCEDURE") and not is_form:
            indentation_level += 1
        if line_stripped.startswith("DEFINE CLASS"):
            indentation_level += 1

        binary_operator_on_two_lines = False
        if continuation_line and re.search(r"([\w)\]'\"])(?<!WITH)(?<!STEP)(?<!SKIP)\s+;", line_stripped):
            binary_operator_on_two_lines = True

        if comment_start != -1:
            corrected_line = corrected_line + " " + comment

        if is_report_expr and len(corrected_line) > 254:
            corrected_lines.append(line.strip())
        else:
            corrected_lines.append(corrected_line)

    return corrected_lines


if __name__ == "__main__":
    app()
