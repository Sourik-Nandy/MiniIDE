import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    code = ""
    language = "python"

    if request.method == "POST":
        code = request.form["code"]
        language = request.form["language"]

        # ---------- PYTHON ----------
        if language == "python":
            try:
                result = subprocess.run(
                    ["python", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout if result.stdout else result.stderr
            except Exception as e:
                output = str(e)

        # ---------- JAVA ----------
        elif language == "java":
            filename = "temp/Main.java"   # Always save as Main.java
            classname = "Main"
            try:
                # Save code
                with open(filename, "w") as f:
                    f.write(code)

                # Compile
                compile_proc = subprocess.run(
                    ["javac", filename],
                    capture_output=True,
                    text=True
                )

                if compile_proc.returncode != 0:
                    output = compile_proc.stderr
                else:
                    # Run class
                    run_proc = subprocess.run(
                        ["java", "-cp", "temp", classname],
                        capture_output=True,
                        text=True
                    )
                    output = run_proc.stdout if run_proc.stdout else run_proc.stderr

            except Exception as e:
                output = str(e)

            finally:
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)
                class_file = f"temp/{classname}.class"
                if os.path.exists(class_file):
                    os.remove(class_file)

        # ---------- C ----------
        elif language == "c":
            filename = "temp/program.c"
            exe_file = "temp/program.exe"
            try:
                with open(filename, "w") as f:
                    f.write(code)

                # Compile
                compile_proc = subprocess.run(
                    ["gcc", filename, "-o", exe_file],
                    capture_output=True,
                    text=True
                )

                if compile_proc.returncode != 0:
                    output = compile_proc.stderr
                else:
                    run_proc = subprocess.run(
                        [exe_file],
                        capture_output=True,
                        text=True
                    )
                    output = run_proc.stdout if run_proc.stdout else run_proc.stderr

            except Exception as e:
                output = str(e)

            finally:
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)
                if os.path.exists(exe_file):
                    os.remove(exe_file)

    return render_template("index.html", output=output, code=code, language=language)

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)  # ensure temp folder exists
    app.run(debug=True)
