package com.example.py2apk;

public class APIKeyManager {
    public static String getApiKey() {
        try {
            return System.getenv("AI_API_KEY");
        } catch (Exception e) {
            return "";
        }
    }
}
