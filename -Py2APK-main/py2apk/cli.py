"""Command-line interface for Py2APK"""
import click
import logging
import sys
from pathlib import Path
from .builder import APKBuilder
from .analyzer import DependencyAnalyzer
from .gui.main_window import launch_gui, MainWindow


from logging.handlers import QueueHandler, QueueListener

# Default logging configuration for CLI
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--project", help="Path to Python project directory")
@click.option("--output", default="dist", help="Output directory for APK")
@click.option("--gui", is_flag=True, help="Launch graphical interface")
def main(project, output, gui):
    """
    Convert Python AI projects to Android APKs
    
    Args:
        project (str): Path to project directory
        output (str): Output directory path
        gui (bool): Launch GUI interface
    """
    try:
        if gui:
            root_logger = logging.getLogger()
            window = MainWindow()
            queue_handler = QueueHandler(window.log_queue)
            root_logger.addHandler(queue_handler)
            launch_gui()
        else:
            if not project:
                logger.error("Please specify a project path with --project")
                sys.exit(1)
                
            project_path = Path(project)
            output_path = Path(output)
            
            if not validate_project(project_path):
                sys.exit(1)
                
            builder = APKBuilder(project_path, output_path)
            if builder.create_android_project():
                logger.info("Android project created successfully.")
                if builder.build_apk():
                    logger.info(f"APK successfully built: {output_path}/app-release.apk")
                else:
                    logger.error("APK build failed.")
            else:
                logger.error("Android project creation failed.")
                
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        sys.exit(1)

def validate_project(project_path: Path) -> bool:
    """
    Validate project structure
    
    Args:
        project_path (Path): Path to project directory
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_files = ["main.py"]
    for f in required_files:
        if not (project_path / f).exists():
            logger.error(f"Missing required file: {f}")
            return False
    
    analyzer = DependencyAnalyzer()
    issues = analyzer.check_compatibility(project_path / "requirements.txt")
    if issues:
        logger.warning("Dependency compatibility issues found:")
        for issue in issues:
            logger.warning(f"- {issue}")
            
    return True

if __name__ == "__main__":
    main()
