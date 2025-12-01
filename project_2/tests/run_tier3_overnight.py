"""
Tier 3 Overnight Test Runner

This script runs both mega-scale tests sequentially:
1. tier3_mega_scale_test.py (YouTube, LiveJournal, Orkut) - ~6-12 hours
2. tier3_friendster_test.py (Friendster moonshot) - ~3-9 hours

Designed to run unattended overnight with comprehensive logging.

Total estimated time: 9-21 hours
Expected completion: Next morning

Date: November 30, 2025
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time
import signal


class TestRunner:
    """Manages sequential execution of Tier 3 tests with logging."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results_dir = self.project_root / 'results'
        self.logs_dir = self.results_dir / 'logs'
        self.start_time = None
        self.interrupted = False

        # Create directories
        self.results_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n\n⚠️  INTERRUPT SIGNAL RECEIVED")
        print("Allowing current test to complete gracefully...")
        print("Press Ctrl+C again to force quit (not recommended)")
        self.interrupted = True

    def _get_timestamp(self):
        """Get current timestamp string."""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def _get_log_filename(self, test_name):
        """Generate log filename with timestamp."""
        timestamp = self._get_timestamp()
        return self.logs_dir / f"{test_name}_{timestamp}.log"

    def _run_test(self, script_name, test_description, estimated_hours):
        """
        Run a single test script with output logging.

        Args:
            script_name: Name of the test script (e.g., 'tier3_mega_scale_test.py')
            test_description: Human-readable description
            estimated_hours: Estimated runtime in hours

        Returns:
            tuple: (success: bool, runtime_seconds: float)
        """
        print(f"\n{'='*80}")
        print(f"STARTING: {test_description}")
        print(f"Script: {script_name}")
        print(f"Estimated time: {estimated_hours} hours")
        print(f"{'='*80}\n")

        script_path = Path(__file__).parent / script_name
        log_file = self._get_log_filename(script_name.replace('.py', ''))

        print(f"📝 Logging output to: {log_file}")
        print(f"🕐 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        estimated_end = datetime.now() + timedelta(hours=estimated_hours)
        print(f"⏰ Estimated completion: {estimated_end.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        start_time = time.time()

        try:
            # Run test with real-time output to both console and log file
            with open(log_file, 'w') as f:
                # Write header to log file
                f.write(f"{'='*80}\n")
                f.write(f"Test: {test_description}\n")
                f.write(f"Script: {script_name}\n")
                f.write(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")
                f.flush()

                # Run the test
                process = subprocess.Popen(
                    [sys.executable, str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )

                # Stream output to both console and file
                for line in process.stdout:
                    print(line, end='')  # Print to console
                    f.write(line)  # Write to log file
                    f.flush()

                # Wait for completion
                process.wait()

            runtime = time.time() - start_time
            runtime_hours = runtime / 3600

            print(f"\n{'='*80}")
            if process.returncode == 0:
                print(f"✅ SUCCESS: {test_description}")
                print(f"   Runtime: {runtime:.2f}s ({runtime_hours:.2f} hours)")
                print(f"   End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Log file: {log_file}")
                print(f"{'='*80}\n")
                return True, runtime
            else:
                print(f"❌ FAILED: {test_description}")
                print(f"   Exit code: {process.returncode}")
                print(f"   Runtime: {runtime:.2f}s ({runtime_hours:.2f} hours)")
                print(f"   Log file: {log_file}")
                print(f"{'='*80}\n")
                return False, runtime

        except Exception as e:
            runtime = time.time() - start_time
            print(f"\n{'='*80}")
            print(f"❌ ERROR: {test_description}")
            print(f"   Exception: {str(e)}")
            print(f"   Runtime: {runtime:.2f}s ({runtime/3600:.2f} hours)")
            print(f"   Log file: {log_file}")
            print(f"{'='*80}\n")
            return False, runtime

    def run_all_tests(self):
        """Run all Tier 3 tests sequentially."""
        print("\n" + "="*80)
        print("TIER 3 OVERNIGHT TEST SUITE")
        print("="*80)
        print()
        print("This will run TWO test suites sequentially:")
        print("  1. Mega-Scale Tests (YouTube, LiveJournal, Orkut)")
        print("  2. Friendster Moonshot Test")
        print()
        print("⚠️  WARNING: This will take 9-21 hours to complete!")
        print()
        print("All output will be logged to:")
        print(f"  {self.logs_dir}/")
        print()
        print("Results will be saved to:")
        print(f"  {self.results_dir}/tier3_mega_scale_results.csv")
        print(f"  {self.results_dir}/tier3_friendster_results.csv")
        print()
        print("You can safely close your terminal - tests will continue running.")
        print("To monitor progress later, use: tail -f results/logs/<latest_log_file>")
        print()
        print("="*80)
        print()

        # Ask for confirmation
        try:
            response = input("Ready to start overnight tests? [y/N]: ").strip().lower()
            if response != 'y':
                print("Aborted by user.")
                return
        except KeyboardInterrupt:
            print("\nAborted by user.")
            return

        self.start_time = time.time()
        overall_start = datetime.now()

        print(f"\n🚀 STARTING OVERNIGHT TEST SUITE")
        print(f"   Start time: {overall_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        results = []

        # Test 1: Mega-Scale Tests
        if not self.interrupted:
            success, runtime = self._run_test(
                'tier3_mega_scale_test.py',
                'Mega-Scale Tests (YouTube, LiveJournal, Orkut)',
                estimated_hours=9
            )
            results.append(('Mega-Scale Tests', success, runtime))

            if self.interrupted:
                print("\n⚠️  Tests interrupted after Mega-Scale suite")
                print("Friendster test will be skipped.")

        # Test 2: Friendster Moonshot (only if not interrupted)
        if not self.interrupted:
            success, runtime = self._run_test(
                'tier3_friendster_test.py',
                'Friendster Moonshot Test',
                estimated_hours=9
            )
            results.append(('Friendster Moonshot', success, runtime))

        # Final summary
        overall_runtime = time.time() - self.start_time
        overall_hours = overall_runtime / 3600
        overall_end = datetime.now()

        print("\n" + "="*80)
        print("OVERNIGHT TEST SUITE COMPLETE")
        print("="*80)
        print()
        print(f"Start time:  {overall_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End time:    {overall_end.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total time:  {overall_runtime:.2f}s ({overall_hours:.2f} hours)")
        print()
        print("RESULTS SUMMARY:")
        print()

        for test_name, success, runtime in results:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            runtime_hours = runtime / 3600
            print(f"  {status} - {test_name}")
            print(f"    Runtime: {runtime:.2f}s ({runtime_hours:.2f} hours)")

        print()
        print("OUTPUT FILES:")
        print(f"  Results: {self.results_dir}/")
        print(f"  Logs:    {self.logs_dir}/")
        print()

        # Count successes
        successes = sum(1 for _, success, _ in results if success)
        total = len(results)

        print(f"Overall: {successes}/{total} test suites completed successfully")
        print()
        print("="*80)

        if successes == total and not self.interrupted:
            print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            print("Your results are ready for analysis.")
        elif self.interrupted:
            print("⚠️  Tests were interrupted - some results may be incomplete")
        else:
            print("⚠️  Some tests failed - check log files for details")

        print("="*80)
        print()


def main():
    """Main entry point."""
    runner = TestRunner()
    runner.run_all_tests()


if __name__ == '__main__':
    main()
