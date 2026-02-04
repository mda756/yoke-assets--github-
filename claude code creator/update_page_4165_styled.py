"""
Update Society Membership Draft Page 4165 - With Proper Styling
Uses styling patterns from page 4146
"""

from wordpress_client import WordPressClient

def main():
    """Update page 4165 with properly styled Medical Societies content"""
    client = WordPressClient()
    page_id = 4165

    print(f"Updating page {page_id} with STYLED content...")

    panels = []

    # HERO PANEL - Medical Societies
    panels.append({
        "acf_fc_layout": "hero",
        "image_positioning": False,
        "hero_image": 4063,  # Using existing image
        "hero_title": "Your Members Pay for CPD. Can You Identify Their Gaps AND Prove You're Closing Them?",
        "hero_content": "<h3><span style=\"color: #ffffff;\">Most societies track credits. But Yoke identifies clinical gaps, creates pathways to close them, and proves it's working—with better engagement driving better insights.</span></h3>",
        "hero_button": "Book a 30-Minute Meeting",
        "hero_link": "/contact"
    })

    # TWO COL PANEL - Three Questions (with image)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": 3639,  # Using existing image
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """
<h1><span style="color: #00ffff;">THREE QUESTIONS YOU CAN'T ANSWER</span></h1>

<h3><span style="color: #003366;"><strong>1. Which gaps exist—and how do we close them?</strong></span></h3>
<span style="color: #003366;">
You track credits earned. But you can't identify which clinical knowledge gaps your members have, create targeted pathways to close them, or measure whether it's working.
</span>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>The Data:</strong></span> 95% of CPD measures knowledge. Only 46% measures practice performance. <em>(ACCME 2024)</em></span></p>

<h3><span style="color: #003366;"><strong>2. How do we get better engagement AND better insights?</strong></span></h3>
<span style="color: #003366;">
Low engagement means poor data. You can't understand member needs because they're not actively using your platform. And without insights, you can't improve engagement. You're stuck in a loop.
</span>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>The Problem:</strong></span> Evidence takes 17 years to change practice—but you can't prove you're accelerating that. <em>(JAMA 2023)</em></span></p>

<h3><span style="color: #003366;"><strong>3. How do we prove it's working?</strong></span></h3>
<span style="color: #003366;">
Without engagement data, practice application tracking, and gap-closure metrics, you can't demonstrate value. Activity stats don't show whether members improved.
</span>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>The Research:</strong></span> "Education alone rarely changes practice." You need application support and proof. <em>(BMC Medical Education 2024)</em></span></p>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # CONTENT PANEL - Vicious Cycle
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "center",
        "background_colour": False,
        "content_block": """
<h2><span style="color: #00ffff;">The Vicious Cycle</span></h2>
<h3><span style="color: #003366;">Low Engagement = Poor Insights = Can't Prove Value</span></h3>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>For Members:</strong></span> Generic library. No guidance on closing THEIR gaps. Complete credits elsewhere.</span></p>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>For Your Board:</strong></span> Activity metrics only. Can't prove gaps identified or closed. Can't justify investment.</span></p>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>For You:</strong></span> Low engagement. No insights. Guesswork strategy. Can't demonstrate value.</span></p>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "large"
    })

    # TWO COL PANEL - Virtuous Cycle
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": False,
        "alignment": False,
        "width": "third",
        "image_two_col": 3639,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """
<h1><span style="color: #00ffff;">THE VIRTUOUS CYCLE</span></h1>
<p><span style="color: #003366;"><strong>Gap Identification → Closure Pathways → Better Engagement → Better Insights → More Effective Gap Closure</strong></span></p>

<h3><span style="color: #003366;"><strong>How It Works Together:</strong></span></h3>

<h4><span style="color: #ff6600;"><strong>1. Gap Identification</strong></span></h4>
<span style="color: #003366;">
<strong>Members complete brief assessment.</strong><br>
Platform identifies clinical knowledge gaps and confidence deficits.
<br><br>
<strong>You see aggregate insights.</strong><br>
Which topics show gaps across your membership. Where content is needed.
</span>

<h4><span style="color: #ff6600;"><strong>2. Ability to Close Those Gaps</strong></span></h4>
<span style="color: #003366;">
<strong>Personalized pathways.</strong><br>
Instead of "browse all content," members see: "Based on your gaps, complete these modules."
<br><br>
<strong>Application support.</strong><br>
Not just theory. Case scenarios, practice tracking, progress visualization.
<br><br>
<strong>Targeted content creation.</strong><br>
Know exactly what gaps exist—create content that addresses them.
</span>

<h4><span style="color: #ff6600;"><strong>3. Better Engagement</strong></span></h4>
<span style="color: #003366;">
<strong>Because it's personalized.</strong><br>
Members engage more when they see which content closes THEIR gaps.
<br><br>
<strong>Give-to-get.</strong><br>
Give assessment. Get personalized dashboard and recommendations. Immediate value.
<br><br>
<strong>Progress tracking.</strong><br>
Visual timeline of improvement. Certificate pathways tied to gap closure.
</span>

<h4><span style="color: #ff6600;"><strong>4. Better Insights & Proof</strong></span></h4>
<span style="color: #003366;">
<strong>Higher engagement = richer data.</strong><br>
More members using platform = better understanding of what works.
<br><br>
<strong>Gap-closure tracking.</strong><br>
Which modules help members improve confidence and apply learning.
<br><br>
<strong>Content performance.</strong><br>
Which topics drive engagement. Which formats work best. What gaps remain.
</span>

<h4><span style="color: #ff6600;"><strong>5. More Effective Gap Closure</strong></span></h4>
<span style="color: #003366;">
<strong>Data improves strategy.</strong><br>
Know which content works. Double down on high-impact modules.
<br><br>
<strong>Better engagement = better outcomes.</strong><br>
Members complete pathways. Apply learning. Report improvements.
<br><br>
<strong>Proof for board and members.</strong><br>
"Gaps identified, pathways created, engagement increased, improvement tracked."
</span>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # CONTENT PANEL - The Cycle Summary
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "center",
        "background_colour": False,
        "content_block": """
<h2><span style="color: #00ffff;">The Cycle</span></h2>
<p><span style="color: #003366;">
→ Identify gaps<br>
→ Create personalized pathways to close them<br>
→ Better engagement (because personalized)<br>
→ Better insights (from engagement data)<br>
→ More effective gap closure (informed by insights)<br>
→ Better metrics proving value<br>
→ Improved member retention
</span></p>
<p><span style="color: #ff6600;"><strong>Not separate pieces. An integrated system.</strong></span></p>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "large"
    })

    # TWO COL PANEL - What You Get (with custom ticks!)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "half",
        "image_two_col": None,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """
<h2><span style="color: #00ffff;">WHAT YOU GET</span></h2>

<h4><span style="color: #ff6600;"><strong>Gap Identification:</strong></span></h4>
<ul class="custom-ticks yellow" style="margin: 0;">
    <li><span style="color: #003366;">Know which topics members struggle with</span></li>
    <li><span style="color: #003366;">Aggregate patterns across membership</span></li>
    <li><span style="color: #003366;">Personal dashboards for each member</span></li>
</ul>

<h4><span style="color: #ff6600;"><strong>Ability to Close Gaps:</strong></span></h4>
<ul class="custom-ticks yellow" style="margin: 0;">
    <li><span style="color: #003366;">Personalized pathways</span></li>
    <li><span style="color: #003366;">Application support, not just theory</span></li>
    <li><span style="color: #003366;">Targeted content strategy</span></li>
</ul>

<h4><span style="color: #ff6600;"><strong>Better Engagement:</strong></span></h4>
<ul class="custom-ticks yellow" style="margin: 0;">
    <li><span style="color: #003366;">Higher participation (personalized = relevant)</span></li>
    <li><span style="color: #003366;">Better completion rates</span></li>
    <li><span style="color: #003366;">Members return to track progress</span></li>
</ul>

<h4><span style="color: #ff6600;"><strong>Better Insights & Proof:</strong></span></h4>
<ul class="custom-ticks yellow" style="margin: 0;">
    <li><span style="color: #003366;">Which content works</span></li>
    <li><span style="color: #003366;">Gap-closure tracking</span></li>
    <li><span style="color: #003366;">Evidence of member improvement</span></li>
</ul>

<h4><span style="color: #ff6600;"><strong>Better Metrics:</strong></span></h4>
<ul class="custom-ticks yellow" style="margin: 0;">
    <li><span style="color: #003366;">Platform performance improves with engagement</span></li>
    <li><span style="color: #003366;">Richer data drives better decisions</span></li>
    <li><span style="color: #003366;">Demonstrable value for board and members</span></li>
</ul>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # CONTENT PANEL - 4 Steps
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "left",
        "background_colour": False,
        "content_block": """
<h2><span style="color: #00ffff;">4 STEPS TO START THE VIRTUOUS CYCLE</span></h2>
<ol>
<li><span style="color: #003366;"><span style="color: #ff6600;"><strong>Gap Assessment</strong></span> → Members identify their clinical knowledge gaps</span></li>
<li><span style="color: #003366;"><span style="color: #ff6600;"><strong>Personalized Pathways</strong></span> → Platform recommends content to close those specific gaps</span></li>
<li><span style="color: #003366;"><span style="color: #ff6600;"><strong>Engagement + Tracking</strong></span> → Members complete pathways, track progress, apply learning</span></li>
<li><span style="color: #003366;"><span style="color: #ff6600;"><strong>Insights + Improvement</strong></span> → You see what works, refine strategy, close more gaps effectively</span></li>
</ol>
<p><span style="color: #003366;"><strong>Timeline:</strong> 2-4 weeks to launch.</span></p>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # CONTENT PANEL - Why It Works
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "left",
        "background_colour": False,
        "content_block": """
<h2><span style="color: #00ffff;">WHY IT WORKS - BUILT ON RESEARCH</span></h2>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>ACCME 2024:</strong></span> 95% of CPD measures knowledge only. We add gap identification, practice application, and closure tracking.</span></p>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>JAMA 2023:</strong></span> Evidence takes 17 years to change practice. We identify where members struggle and create targeted pathways to accelerate adoption.</span></p>

<p><span style="color: #003366;"><span style="color: #ff6600;"><strong>BMC Medical Education 2024:</strong></span> Education alone doesn't work. We add personalized pathways, application support, and engagement strategies that drive proof.</span></p>
        """
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # SMALL CTA BANNER - Awards/Proof
    panels.append({
        "acf_fc_layout": "small_cta_banner",
        "reverse_panel": False,
        "content_type": "nobutton",
        "image_cta_small": 2693,  # Using awards image from page 4146
        "content_cta_small": """
<h2><span style="color: #f79801;">Proven Platform</span></h2>
<strong><span style="color: #f79801;">3 MAJOR INDUSTRY AWARDS FOR MEASURABLE IMPACT</span></strong>
<span style="font-weight: 400;">Recognized for innovation in healthcare education and digital communication</span>

<strong><span style="color: #f79801;">10+ PROGRAMS ACROSS 6+ MARKETS</span></strong>
<span style="font-weight: 400;">Deployed globally with proven outcomes measurement</span>

<strong><span style="color: #f79801;">BUILT ON PEER-REVIEWED RESEARCH (2023-2025)</span></strong>
<span style="font-weight: 400;">Evidence-based approach to CPD outcomes and behavior change</span>
        """,
        "cta_button_small": "",
        "cta_link_small": ""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "large"
    })

    # CONTENT PANEL - Final CTA
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "center",
        "background_colour": False,
        "content_block": """
<h2><span style="color: #00ffff;">SEE THE INTEGRATED SYSTEM IN ACTION</span></h2>
<p><span style="color: #003366;">Book a 30-minute meeting to see: Gap identification + closure pathways, How personalization drives engagement, Insights dashboard showing what works, How better engagement creates better metrics</span></p>
<p style="text-align: center;"><a class="button" href="/contact">Book Your 30-Minute Meeting</a></p>
        """
    })

    print(f"Created {len(panels)} styled ACF panels")

    # Update page
    try:
        result = client.post(
            f"pages/{page_id}",
            data={
                "acf": {
                    "panels": panels
                },
                "status": "draft"
            }
        )

        print("SUCCESS: Page updated with styled content!")
        print(f"View at: https://yokehealth.com/?page_id={page_id}&preview=true")
        print(f"Edit at: https://yokehealth.com/wp-admin/post.php?post={page_id}&action=edit")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
