#!/usr/bin/env python3
"""
Launcher for the encrypted credit risk predictor application.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    try:
        # Set up paths
        base_dir = Path(__file__).parent
        dist_dir = base_dir / 'dist'
        
        # Check if dist directory exists
        if not dist_dir.exists():
            print("Error: 'dist' directory not found. Please run encrypt_project.py first.")
            sys.exit(1)
            
        # Check if PyArmor runtime exists
        if not (dist_dir / 'pyarmor_runtime_000000').exists():
            print("Error: PyArmor runtime not found. Please run encrypt_project.py first.")
            sys.exit(1)
        
        # Add dist directory to Python path
        runtime_path = str(dist_dir / 'pyarmor_runtime_000000')
        if runtime_path not in sys.path:
            sys.path.insert(0, runtime_path)
        
        # Import PyArmor runtime
        try:
            # Add the parent directory to sys.path
            if str(dist_dir) not in sys.path:
                sys.path.insert(0, str(dist_dir))
                
            import pyarmor_runtime_000000
        except ImportError as e:
            print(f"Error importing PyArmor runtime: {e}")
            print("Make sure you've run encrypt_project.py first.")
            sys.exit(1)
            
        print("Starting encrypted credit risk predictor...")
        
        # Run Streamlit using subprocess
        app_path = str(dist_dir / 'app.py')
        cmd = [sys.executable, '-m', 'streamlit', 'run', '--server.headless', 'true', '--server.runOnSave', 'true', app_path]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Streamlit: {e}", file=sys.stderr)
            sys.exit(e.returncode)
            
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
