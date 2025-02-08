# Py2APK

Py2APK is an Android application that demonstrates how to run Python code, specifically an ONNX AI model, within an Android app using Chaquopy.

## Overview

This project showcases the integration of a Python-based AI model into an Android environment. It utilizes Chaquopy to execute Python code and ONNX Runtime for model inference. The application loads the model path dynamically from a configuration file (`frontend-config.json`).

## Project Structure

- `py2apk/`: Contains the main project files.
  - `android_project/`: The Android project directory.
    - `app/src/main/`:
      - `java/com/example/py2apk/`: Java source code.
        - `MainActivity.java`: Main activity of the app.
        - `PythonBridge.java`: Handles communication with Python.
        - `MyApplication.java`: Custom Application class to get application context.
        - `AIService.java`: Foreground service for AI processing.
      - `python/`: Python source code.
        - `ai_model.py`: Loads and runs the ONNX model.
      - `AndroidManifest.xml`: Android manifest file.
      - `res/`: Resources for the Android app.
  - `utils/`: Utility scripts.
    - `ai_processing.py`: Processes input and interacts with the AI model.
- `frontend-config.json`: Configuration file for the frontend, including the model path.

## Setup

1. **Prerequisites:**
   - Android Studio installed and configured.
   - Python 3.8+ installed.
   - Chaquopy plugin configured in the Android project (see `build.gradle` files).
   - ONNX Runtime installed (managed by Chaquopy).

2. **Building the Project:**
   - Open the `py2apk/android_project` directory in Android Studio.
   - Build the project using the "Build" menu.

3. **Configuration:**
   - Modify `frontend-config.json` to specify the path to your ONNX model:

   ```json
   {
       "model_path": "path/to/your/model.onnx"
   }
   ```

   Place the model file in the `app/src/main/assets` folder.

4. **Running the Application:**
   - Connect an Android device or use an emulator.
   - Run the application from Android Studio.

## Usage

The application takes input in the form of a JSON string, passes it to the Python script, which uses ONNX runtime to perform inference, and returns the result as a JSON string. The communication between Java and Python is handled by Chaquopy.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
