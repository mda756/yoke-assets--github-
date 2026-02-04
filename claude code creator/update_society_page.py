"""
Update Society Membership Draft Page (ID 4159)
Pushes the landing page content to WordPress
"""

from wordpress_client import WordPressClient

def create_landing_page_panels():
    """Build ACF panels for the landing page"""
    client = WordPressClient()
    panels = []

    # HERO SECTION
    panels.append(client.build_hero_panel(
        title="Your Members Pay for CPD. Can You Identify Their Gaps AND Prove You're Closing Them?",
        subtitle="Most societies track credits. But you can't identify which clinical gaps exist, create pathways to close them, or prove it's working. Our system does all three—and better engagement drives better insights, which drives more effective gap closure.",
        button_text="Book a 30-Minute Meeting",
        button_url="/contact"  # Update with actual booking URL
    ))

    panels.append(client.build_spacing_panel("medium"))

    # PROBLEM SECTION
    panels.append(client.build_content_panel(
        title="Three Questions You Can't Answer",
        content="""
        <h3>1. Which gaps exist—and how do we close them?</h3>
        <p>You track credits earned. But you can't identify which clinical knowledge gaps your members have, create targeted pathways to close them, or measure whether it's working.</p>
        <p><strong>The Data:</strong> 95% of CPD measures knowledge. Only 46% measures practice performance. <em>(ACCME 2024)</em></p>

        <h3>2. How do we get better engagement AND better insights?</h3>
        <p>Low engagement means poor data. You can't understand member needs because they're not actively using your platform. And without insights, you can't improve engagement. You're stuck in a loop.</p>
        <p><strong>The Problem:</strong> Evidence takes 17 years to change practice—but you can't prove you're accelerating that. <em>(JAMA 2023)</em></p>

        <h3>3. How do we prove it's working?</h3>
        <p>Without engagement data, practice application tracking, and gap-closure metrics, you can't demonstrate value. Activity stats don't show whether members improved.</p>
        <p><strong>The Research:</strong> "Education alone rarely changes practice." You need application support and proof. <em>(BMC Medical Education 2024)</em></p>
        """
    ))

    panels.append(client.build_spacing_panel("medium"))

    # CONSEQUENCE
    panels.append(client.build_content_panel(
        title="The Vicious Cycle: Low Engagement = Poor Insights = Can't Prove Value",
        content="""
        <p><strong>For Members:</strong> Generic library. No guidance on closing THEIR gaps. Complete credits elsewhere.</p>
        <p><strong>For Your Board:</strong> Activity metrics only. Can't prove gaps identified or closed. Can't justify investment.</p>
        <p><strong>For You:</strong> Low engagement. No insights. Guesswork strategy. Can't demonstrate value.</p>
        """
    ))

    panels.append(client.build_spacing_panel("large"))

    # SOLUTION SECTION
    panels.append(client.build_content_panel(
        title="The Virtuous Cycle: Gap Identification → Closure Pathways → Better Engagement → Better Insights → More Effective Gap Closure",
        content="""
        <h3>How It Works Together:</h3>

        <h4>1. Gap Identification</h4>
        <p><strong>Members complete brief assessment.</strong><br>
        Platform identifies clinical knowledge gaps and confidence deficits.</p>
        <p><strong>You see aggregate insights.</strong><br>
        Which topics show gaps across your membership. Where content is needed.</p>

        <h4>2. Ability to Close Those Gaps</h4>
        <p><strong>Personalized pathways.</strong><br>
        Instead of "browse all content," members see: "Based on your gaps, complete these modules."</p>
        <p><strong>Application support.</strong><br>
        Not just theory. Case scenarios, practice tracking, progress visualization.</p>
        <p><strong>Targeted content creation.</strong><br>
        Know exactly what gaps exist—create content that addresses them.</p>

        <h4>3. Better Engagement</h4>
        <p><strong>Because it's personalized.</strong><br>
        Members engage more when they see which content closes THEIR gaps.</p>
        <p><strong>Give-to-get.</strong><br>
        Give assessment. Get personalized dashboard and recommendations. Immediate value.</p>
        <p><strong>Progress tracking.</strong><br>
        Visual timeline of improvement. Certificate pathways tied to gap closure.</p>

        <h4>4. Better Insights & Proof</h4>
        <p><strong>Higher engagement = richer data.</strong><br>
        More members using platform = better understanding of what works.</p>
        <p><strong>Gap-closure tracking.</strong><br>
        Which modules help members improve confidence and apply learning.</p>
        <p><strong>Content performance.</strong><br>
        Which topics drive engagement. Which formats work best. What gaps remain.</p>

        <h4>5. More Effective Gap Closure</h4>
        <p><strong>Data improves strategy.</strong><br>
        Know which content works. Double down on high-impact modules.</p>
        <p><strong>Better engagement = better outcomes.</strong><br>
        Members complete pathways. Apply learning. Report improvements.</p>
        <p><strong>Proof for board and members.</strong><br>
        "Gaps identified, pathways created, engagement increased, improvement tracked."</p>
        """
    ))

    panels.append(client.build_spacing_panel("medium"))

    # THE CYCLE
    panels.append(client.build_content_panel(
        title="It works together:",
        content="""
        <p>→ Identify gaps<br>
        → Create personalized pathways to close them<br>
        → Better engagement (because personalized)<br>
        → Better insights (from engagement data)<br>
        → More effective gap closure (informed by insights)<br>
        → Better metrics proving value<br>
        → Improved member retention</p>
        <p><strong>Not separate pieces. An integrated system.</strong></p>
        """
    ))

    panels.append(client.build_spacing_panel("large"))

    # WHAT YOU GET
    panels.append(client.build_content_panel(
        title="What You Get",
        content="""
        <h4>Gap Identification:</h4>
        <ul>
        <li>✅ Know which topics members struggle with</li>
        <li>✅ Aggregate patterns across membership</li>
        <li>✅ Personal dashboards for each member</li>
        </ul>

        <h4>Ability to Close Gaps:</h4>
        <ul>
        <li>✅ Personalized pathways</li>
        <li>✅ Application support, not just theory</li>
        <li>✅ Targeted content strategy</li>
        </ul>

        <h4>Better Engagement:</h4>
        <ul>
        <li>✅ Higher participation (personalized = relevant)</li>
        <li>✅ Better completion rates</li>
        <li>✅ Members return to track progress</li>
        </ul>

        <h4>Better Insights & Proof:</h4>
        <ul>
        <li>✅ Which content works</li>
        <li>✅ Gap-closure tracking</li>
        <li>✅ Evidence of member improvement</li>
        </ul>

        <h4>Better Metrics:</h4>
        <ul>
        <li>✅ Platform performance improves with engagement</li>
        <li>✅ Richer data drives better decisions</li>
        <li>✅ Demonstrable value for board and members</li>
        </ul>
        """
    ))

    panels.append(client.build_spacing_panel("medium"))

    # HOW IT WORKS
    panels.append(client.build_content_panel(
        title="4 Steps to Start the Virtuous Cycle",
        content="""
        <ol>
        <li><strong>Gap Assessment</strong> → Members identify their clinical knowledge gaps</li>
        <li><strong>Personalized Pathways</strong> → Platform recommends content to close those specific gaps</li>
        <li><strong>Engagement + Tracking</strong> → Members complete pathways, track progress, apply learning</li>
        <li><strong>Insights + Improvement</strong> → You see what works, refine strategy, close more gaps effectively</li>
        </ol>
        <p><strong>Timeline:</strong> 2-4 weeks to launch.</p>
        """
    ))

    panels.append(client.build_spacing_panel("medium"))

    # WHY IT WORKS
    panels.append(client.build_content_panel(
        title="Why It Works - Built on Research",
        content="""
        <p><strong>ACCME 2024:</strong> 95% of CPD measures knowledge only. We add gap identification, practice application, and closure tracking.</p>
        <p><strong>JAMA 2023:</strong> Evidence takes 17 years to change practice. We identify where members struggle and create targeted pathways to accelerate adoption.</p>
        <p><strong>BMC Medical Education 2024:</strong> Education alone doesn't work. We add personalized pathways, application support, and engagement strategies that drive proof.</p>
        """
    ))

    panels.append(client.build_spacing_panel("medium"))

    # PROOF
    panels.append(client.build_content_panel(
        title="",
        content="""
        <p>✓ 3 major industry awards for measurable impact<br>
        ✓ 10+ programs across 6+ markets<br>
        ✓ Built on peer-reviewed research (2023-2025)</p>
        """
    ))

    panels.append(client.build_spacing_panel("large"))

    # FINAL CTA
    panels.append(client.build_cta_panel(
        heading="See the Integrated System in Action",
        button_text="Book Your 30-Minute Meeting",
        button_url="/contact",  # Update with actual booking URL
        subtext="Book a 30-minute meeting to see: Gap identification + closure pathways, How personalization drives engagement, Insights dashboard showing what works, How better engagement creates better metrics"
    ))

    return panels


def main():
    """Update the WordPress page"""
    client = WordPressClient()
    page_id = 4159

    print(f"Updating page {page_id}...")

    # Build panels
    panels = create_landing_page_panels()

    print(f"Created {len(panels)} ACF panels")

    # Update page
    try:
        result = client.update_page(
            page_id=page_id,
            acf_panels=panels,
            status="draft"  # Keep as draft
        )

        print(f"✅ Page updated successfully!")
        print(f"View at: https://yokehealth.com/?page_id={page_id}&preview=true")

    except Exception as e:
        print(f"❌ Error updating page: {e}")
        raise


if __name__ == "__main__":
    main()
