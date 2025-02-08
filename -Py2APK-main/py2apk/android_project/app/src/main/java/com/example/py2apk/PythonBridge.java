package com.example.py2apk;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import org.json.JSONObject;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;


public class PythonBridge {
    private static PythonBridge instance;
    private Python python;
    private String modelPath;

    private PythonBridge() {
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(MyApplication.getContext()));
        }
        python = Python.getInstance();
        modelPath = loadModelPath();
    }

    public static PythonBridge getInstance() {
        if (instance == null) {
            instance = new PythonBridge();
        }
        return instance;
    }
    
    private String loadModelPath() {
        try {
            InputStream is = MyApplication.getContext().getAssets().open("frontend-config.json");
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            String jsonString = new String(buffer, StandardCharsets.UTF_8);
            JSONObject jsonObject = new JSONObject(jsonString);
            return jsonObject.getString("model_path");
        } catch (Exception e) {
            e.printStackTrace();
            return "models/placeholder.onnx"; // Default path
        }
    }

    public String runPythonScript(String scriptName, String input) {
        PyObject pyObject = python.getModule(scriptName);
        return pyObject.callAttr("process_input", input, modelPath).toString();
    }
}
