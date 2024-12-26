from flask import Flask, render_template, request, jsonify, Response
import subprocess
import os

app = Flask(__name__)
current_dir = os.getcwd()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    global current_dir
    command = request.json.get('command')
    try:

        if command.startswith('cd '):
            new_dir = command.split('cd ', 1)[1]
            if os.path.isdir(new_dir):
                current_dir = os.path.join(current_dir, new_dir)
            return ''

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=current_dir,
            universal_newlines=True
        )
        def generate():
            for line in iter(process.stdout.readline, ''):
                yield line
            process.stdout.close()
            process.wait()
        
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        return jsonify({'output': str(e)})







if __name__ == '__main__':
    app.run(debug=True)
