"""APK building functionality"""
import subprocess
import logging
import os
from pathlib import Path
from typing import Optional, Callable
from .config import DEFAULT_CONFIG, find_android_sdk
from .signing import APKSigner

logger = logging.getLogger(__name__)


class APKBuilder:
    """Handles Android project creation and APK building"""

    def __init__(self, project_path: Path, output_dir: Path):
        """
        Initialize builder

        Args:
            project_path (Path): Source Python project path
            output_dir (Path): Output directory for APK
        """
        self.project_path = project_path
        self.output_dir = output_dir
        self.android_sdk = find_android_sdk()
        self.apk_signer = APKSigner() # Instantiate APKSigner

    def create_android_project(self) -> bool:
        """Create Chaquopy Android project structure"""
        try:
            # Create directory structure
            (self.output_dir / "app/src/main/python").mkdir(parents=True, exist_ok=True)
            
            # Copy project files
            subprocess.run(
                ["cp", "-r", f"{self.project_path}/*", 
                 f"{self.output_dir}/app/src/main/python/"],
                check=True
            )
            
            # Generate Gradle config
            self._generate_gradle_config()
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Project creation failed: {str(e)}")
            return False

    def _generate_gradle_config(self):
        """Generate Android build configuration"""
        gradle_template = f"""
        android {{
            compileSdk {DEFAULT_CONFIG['PYTHON_VERSION']}
            ndkVersion "25.1.8937393"
            
            defaultConfig {{
                minSdk 21
                targetSdk 33
                python {{
                    version "{DEFAULT_CONFIG['PYTHON_VERSION']}"
                }}
            }}
        }}
        """
        (self.output_dir / "build.gradle").write_text(gradle_template)

    def build_apk(self, callback: Optional[Callable] = None) -> bool:
        """
        Build APK package
        
        Args:
            callback (Callable): Progress callback function
            
        Returns:
            bool: True if build successful
        """
        try:
            gradle_script = "./gradlew"
            if os.name == 'nt': # Windows
                gradle_script = "gradlew.bat"
                
            result = subprocess.run(
                [gradle_script, "assembleRelease"],
                cwd=self.output_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            if callback:
                for line in result.stdout.splitlines():
                    callback(line.strip())

            apk_file = self.output_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release-unsigned.apk"
            keystore_path = Path("debug.keystore") # Placeholder - should be configurable
            keystore_pass = "android" # Placeholder - should be configurable
            key_alias = "androiddebugkey" # Placeholder - should be configurable
            key_pass = "android" # Placeholder - should be configurable

            if not keystore_path.exists():
                logger.info("Generating debug keystore...")
                self.apk_signer.generate_keystore(keystore_path, keystore_pass, key_alias, key_pass)

            if self.apk_signer.sign_apk(apk_file, keystore_path, keystore_pass, key_alias, key_pass):
                logger.info("APK signing completed.")
            else:
                logger.error("APK signing failed.")
                return False
                    
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Build failed: {e.stdout}")
            return False
