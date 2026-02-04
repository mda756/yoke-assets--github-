"""
Pain Discussion Monitor
Monitors Reddit, Twitter, forums for pain discussions matching ICP criteria
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

class PainMonitor:
    """Monitor pain discussions across multiple sources"""

    def __init__(self):
        self.results = []

    def search_reddit(self, subreddit, pain_keywords, intent_phrases, days_back=30):
        """
        Search Reddit for pain discussions

        Note: Uses Reddit API (requires API credentials for production)
        For now, uses web search as proof of concept
        """
        print(f"\n  Searching r/{subreddit} for pain signals...")

        # Build search query
        pain_terms = " OR ".join([f'"{kw}"' for kw in pain_keywords[:5]])
        query = f'site:reddit.com/r/{subreddit} ({pain_terms})'

        # Use web search (Claude Code's WebSearch tool would be used here)
        # For now, return structure to show what we'd capture

        results = {
            'source': f'reddit:r/{subreddit}',
            'query': query,
            'pain_keywords_matched': pain_keywords[:5],
            'search_date': datetime.now().isoformat(),
            'discussions': [
                # Structure for results:
                # {
                #   'title': 'Post title',
                #   'url': 'reddit.com/...',
                #   'snippet': 'text snippet',
                #   'pain_keywords_found': ['keyword1', 'keyword2'],
                #   'intent_signals': ['looking for platform'],
                #   'score': 0.8
                # }
            ]
        }

        print(f"    Query: {query}")
        print(f"    (Web search would execute here)")

        return results

    def search_twitter(self, hashtag, pain_keywords, intent_phrases, days_back=7):
        """
        Search Twitter/X for pain discussions

        Note: Requires Twitter API credentials for production
        """
        print(f"\n  Searching Twitter {hashtag} for pain signals...")

        results = {
            'source': f'twitter:{hashtag}',
            'pain_keywords': pain_keywords[:5],
            'search_date': datetime.now().isoformat(),
            'tweets': []
        }

        print(f"    Hashtag: {hashtag}")
        print(f"    (Twitter API would execute here)")

        return results

    def search_g2_reviews(self, category, pain_keywords):
        """
        Search G2 reviews for pain discussions

        Uses web search to find G2 reviews mentioning pain points
        """
        print(f"\n  Searching G2 reviews ({category}) for pain signals...")

        pain_terms = " OR ".join([f'"{kw}"' for kw in pain_keywords[:3]])
        query = f'site:g2.com/categories/{category} reviews ({pain_terms})'

        results = {
            'source': f'g2:{category}',
            'query': query,
            'search_date': datetime.now().isoformat(),
            'reviews': []
        }

        print(f"    Query: {query}")
        print(f"    (Web search would execute here)")

        return results

    def score_discussion(self, discussion, pain_keywords, intent_phrases):
        """
        Score a discussion for pain + buying intent

        Returns score 0-1
        """
        score = 0.0
        text = (discussion.get('title', '') + ' ' + discussion.get('snippet', '')).lower()

        # Pain keyword matches (0.6 max)
        pain_matches = sum(1 for kw in pain_keywords if kw.lower() in text)
        score += min(pain_matches * 0.15, 0.6)

        # Intent phrase matches (0.4 max)
        intent_matches = sum(1 for phrase in intent_phrases if phrase.lower() in text)
        score += min(intent_matches * 0.2, 0.4)

        return min(score, 1.0)

    def monitor_pain_signals(self, signal_config):
        """
        Monitor all pain discussion sources for an ICP

        Args:
            signal_config: ICP signal configuration dict

        Returns:
            Aggregated pain signals with scores
        """
        print(f"\nMonitoring pain signals for: {signal_config['icp_name']}")

        pain_signal = None
        for signal in signal_config['priority_signals']:
            if signal['type'] == 'pain_discussions':
                pain_signal = signal
                break

        if not pain_signal:
            print("  No pain discussion config found")
            return []

        pain_keywords = pain_signal['pain_keywords']
        intent_phrases = pain_signal['intent_phrases']
        sources = signal_config['sources'].get('pain_discussions', [])

        all_results = []

        for source in sources:
            if source.startswith('reddit:'):
                subreddit = source.split(':')[1].replace('r/', '')
                results = self.search_reddit(subreddit, pain_keywords, intent_phrases)
                all_results.append(results)

            elif source.startswith('twitter:'):
                hashtag = source.split(':')[1]
                results = self.search_twitter(hashtag, pain_keywords, intent_phrases)
                all_results.append(results)

            elif source.startswith('g2:'):
                category = source.split(':')[1]
                results = self.search_g2_reviews(category, pain_keywords)
                all_results.append(results)

        return all_results

    def export_results(self, results, output_dir, icp_name):
        """Export results to JSON"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)

        filename = f"{icp_name.lower().replace(' ', '_')}_pain_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file = output_dir / filename

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n  Results saved: {output_file.name}")
        return output_file


if __name__ == "__main__":
    import sys

    monitor = PainMonitor()

    if len(sys.argv) < 2:
        print("\nUsage: python pain_monitor.py <config_file>")
        print("Example: python pain_monitor.py research_config/medcomms_signals.json")
    else:
        config_file = Path(sys.argv[1])

        with open(config_file, 'r') as f:
            signal_config = json.load(f)

        results = monitor.monitor_pain_signals(signal_config)

        output_dir = Path(__file__).parent.parent / "research_output"
        monitor.export_results(results, output_dir, signal_config['icp_name'])
