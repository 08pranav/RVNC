#!/usr/bin/env python3
"""
Real vs. Nominal Return Calculator Launcher
Choose between CLI and Web interfaces
"""

import sys
import os
import subprocess

def print_banner():
    """Print the application banner"""
    print("=" * 70)
    print("    REAL vs. NOMINAL RETURN CALCULATOR")
    print("=" * 70)
    print("Financial Concept: Inflation-adjusted return calculation")
    print("Formula: Real Return = ((1 + nominal) / (1 + inflation)) - 1")
    print("=" * 70)

def main():
    """Main launcher function"""
    print_banner()
    
    print("\nChoose your interface:")
    print("1. Command Line Interface (CLI) - Interactive text-based")
    print("2. Web Interface (Flask) - Beautiful browser-based") 
    print("3. Indian Investment Examples - See Rupee-based scenarios")
    print("4. Run Tests - Verify calculations")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\n🖥️  Starting Command Line Interface...")
                print("Tips: Type 'help' for assistance, 'example' for samples, 'quit' to exit")
                print("-" * 50)
                subprocess.run([sys.executable, 'cli_calculator.py'])
                break
                
            elif choice == '2':
                print("\n🌐 Starting Web Interface...")
                print("Opening Flask application at http://localhost:5000")
                print("Press Ctrl+C to stop the server")
                print("-" * 50)
                subprocess.run([sys.executable, 'app.py'])
                break
                
            elif choice == '3':
                print("\n🇮🇳 Indian Investment Examples...")
                print("Showing Indian investment scenarios with Rupee amounts")
                print("-" * 50)
                subprocess.run([sys.executable, 'indian_examples.py'])
                
                # Ask if they want to continue
                continue_choice = input("\nReturn to main menu? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    break
                    
            elif choice == '4':
                print("\n🧪 Running Tests...")
                print("-" * 30)
                subprocess.run([sys.executable, 'test_calculator.py'])
                
                # Ask if they want to continue
                continue_choice = input("\nReturn to main menu? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    break
                    
            elif choice == '5':
                print("\nGoodbye! 👋")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()