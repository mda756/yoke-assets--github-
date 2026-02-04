"""
Research Engine
Orchestrates all signal monitoring and scoring for ICP prospect research
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add monitors to path
sys.path.insert(0, str(Path(__file__).parent / "monitors"))

class ResearchEngine:
    """Main research orchestration engine"""

    def __init__(self):
        self.config_dir = Path(__file__).parent / "research_config"
        self.output_dir = Path(__file__).parent / "research_output"
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def load_icp_config(self, icp_name):
        """Load ICP signal configuration"""
        # Try exact match
        config_file = self.config_dir / f"{icp_name}_signals.json"

        if not config_file.exists():
            # Try fuzzy match
            for file in self.config_dir.glob("*_signals.json"):
                if icp_name.lower() in file.stem.lower():
                    config_file = file
                    break

        if not config_file.exists():
            raise ValueError(f"Config not found for ICP: {icp_name}")

        with open(config_file, 'r') as f:
            return json.load(f)

    def list_available_icps(self):
        """List all ICP configs available"""
        icps = []
        for config_file in self.config_dir.glob("*_signals.json"):
            with open(config_file, 'r') as f:
                config = json.load(f)
                icps.append({
                    'name': config['icp_name'],
                    'id': config['icp_id'],
                    'file': config_file.name
                })
        return icps

    def run_research(self, icp_name, monitors=None):
        """
        Run research for an ICP

        Args:
            icp_name: ICP identifier
            monitors: List of monitor types to run (default: all)
                     ['pain', 'launches', 'conferences', 'hiring', 'funding']

        Returns:
            Research results with scored signals
        """
        # Load config
        config = self.load_icp_config(icp_name)
        print(f"\n{'='*60}")
        print(f"Research Engine: {config['icp_name']}")
        print(f"{'='*60}\n")

        # Determine which monitors to run
        if monitors is None:
            # Run all configured signal types
            monitors = [s['type'] for s in config['priority_signals']]

        results = {
            'icp_id': config['icp_id'],
            'icp_name': config['icp_name'],
            'research_date': datetime.now().isoformat(),
            'monitors_run': monitors,
            'signals': {},
            'scored_prospects': []
        }

        # Run each monitor
        for monitor_type in monitors:
            print(f"\n--- Running {monitor_type} monitor ---")

            if monitor_type == 'pain_discussions':
                results['signals']['pain_discussions'] = self._run_pain_monitor(config)

            elif monitor_type == 'product_launches':
                results['signals']['product_launches'] = self._run_launch_monitor(config)

            elif monitor_type == 'conference_activity':
                results['signals']['conference_activity'] = self._run_conference_monitor(config)

            elif monitor_type == 'hiring_signals':
                results['signals']['hiring_signals'] = self._run_hiring_monitor(config)

            elif monitor_type == 'funding_rounds':
                results['signals']['funding_rounds'] = self._run_funding_monitor(config)

            else:
                print(f"  Monitor not implemented: {monitor_type}")

        # Score and rank prospects
        results['scored_prospects'] = self._score_prospects(config, results['signals'])

        # Export results
        output_file = self._export_results(results, config['icp_name'])

        print(f"\n{'='*60}")
        print(f"Research Complete!")
        print(f"Results saved: {output_file.name}")
        print(f"{'='*60}\n")

        return results

    def _run_pain_monitor(self, config):
        """Run pain discussions monitor"""
        try:
            from pain_monitor import PainMonitor
            monitor = PainMonitor()
            return monitor.monitor_pain_signals(config)
        except Exception as e:
            print(f"  Error running pain monitor: {e}")
            return []

    def _run_launch_monitor(self, config):
        """Run product launches monitor"""
        print("  Launching launch monitor...")
        print("  (Monitor implementation: search press releases, company news)")
        print("  (Would use WebSearch + press release APIs)")
        return {
            'source': 'product_launches',
            'method': 'press_releases + company_news',
            'status': 'framework_ready'
        }

    def _run_conference_monitor(self, config):
        """Run conference activity monitor"""
        print("  Launching conference monitor...")
        print("  (Monitor implementation: search event listings, speaker lists)")
        print("  (Would use conference APIs + web search)")
        return {
            'source': 'conference_activity',
            'method': 'event_listings + speaker_databases',
            'status': 'framework_ready'
        }

    def _run_hiring_monitor(self, config):
        """Run hiring signals monitor"""
        print("  Launching hiring monitor...")
        print("  (Monitor implementation: check company career pages)")
        print("  (Would use company websites + job board APIs)")
        return {
            'source': 'hiring_signals',
            'method': 'company_careers + job_boards',
            'status': 'framework_ready'
        }

    def _run_funding_monitor(self, config):
        """Run funding rounds monitor"""
        print("  Launching funding monitor...")
        print("  (Monitor implementation: Crunchbase API + press releases)")
        print("  (Requires Crunchbase API key)")
        return {
            'source': 'funding_rounds',
            'method': 'crunchbase_api + press_releases',
            'status': 'framework_ready'
        }

    def _score_prospects(self, config, signals):
        """
        Score and rank prospects based on signal strength

        Returns:
            List of scored prospects
        """
        print("\n--- Scoring prospects ---")

        # Get signal weights from config
        signal_weights = {}
        for signal in config['priority_signals']:
            signal_weights[signal['type']] = signal.get('weight', 0.1)

        scored_prospects = []

        # Example scoring logic (would be expanded with real data)
        print(f"  Signal weights configured:")
        for signal_type, weight in signal_weights.items():
            print(f"    - {signal_type}: {weight}")

        print(f"\n  (Scoring logic ready - awaits real signal data)")

        return scored_prospects

    def _export_results(self, results, icp_name):
        """Export research results to JSON"""
        filename = f"{icp_name.lower().replace(' ', '_')}_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file = self.output_dir / filename

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        return output_file

    def print_summary(self, results):
        """Print research results summary"""
        print(f"\n{'='*60}")
        print(f"RESEARCH SUMMARY: {results['icp_name']}")
        print(f"{'='*60}\n")

        print(f"Monitors run: {', '.join(results['monitors_run'])}")
        print(f"Signals collected: {len(results['signals'])}")
        print(f"Scored prospects: {len(results['scored_prospects'])}")

        print(f"\nTop signals by type:")
        for signal_type, signal_data in results['signals'].items():
            if isinstance(signal_data, list):
                print(f"  - {signal_type}: {len(signal_data)} sources monitored")
            else:
                print(f"  - {signal_type}: {signal_data.get('status', 'ready')}")


if __name__ == "__main__":
    engine = ResearchEngine()

    if len(sys.argv) < 2:
        print("\nResearch Engine - ICP Signal Monitoring\n")
        print("Available ICPs:")
        for icp in engine.list_available_icps():
            print(f"  - {icp['name']}")

        print("\nUsage:")
        print("  python research_engine.py <icp_name>")
        print("  python research_engine.py <icp_name> <monitors>")
        print("\nExamples:")
        print("  python research_engine.py medcomms")
        print("  python research_engine.py biotech pain,funding")

    else:
        icp_name = sys.argv[1]

        # Parse monitors if provided
        monitors = None
        if len(sys.argv) > 2:
            monitors = [m.strip() for m in sys.argv[2].split(',')]

        results = engine.run_research(icp_name, monitors=monitors)
        engine.print_summary(results)
