"""
Update Page 4165 - Final Version with Alternating Images
Left-aligned, proper spacing, images alternating left/right
"""

from wordpress_client import WordPressClient

def main():
    client = WordPressClient()
    page_id = 4165

    print(f"Updating page {page_id} with proper images and alignment...")

    panels = []

    # HERO PANEL
    panels.append({
        "acf_fc_layout": "hero",
        "image_positioning": False,
        "hero_image": 4063,
        "hero_title": "Your Members Pay for CPD. Can You Identify Their Gaps AND Prove You're Closing Them?",
        "hero_content": "<h3><span style=\"color: #ffffff;\">Most societies track credits. But Yoke identifies clinical gaps, creates pathways to close them, and proves it's working—with better engagement driving better insights.</span></h3>",
        "hero_button": "Book a 30-Minute Meeting",
        "hero_link": "/contact"
    })

    # TWO COL - Three Questions (Image RIGHT, reverse=True)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": 3639,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>Three Questions You Can't Answer</strong></span></h1>
<p>You track CPD credits. But can you prove what's working?</p>
<p>Here's what most medical societies struggle to demonstrate:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Which clinical gaps exist—and how do we close them?</strong> You track credits earned. But you can't identify which clinical knowledge gaps your members have, create targeted pathways to close them, or measure whether it's working.</li>
<li><strong>How do we get better engagement AND better insights?</strong> Low engagement means poor data. You can't understand member needs because they're not actively using your platform. And without insights, you can't improve engagement. You're stuck in a loop.</li>
<li><strong>How do we prove it's working?</strong> Without engagement data, practice application tracking, and gap-closure metrics, you can't demonstrate value. Activity stats don't show whether members improved.</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>The data speaks: 95% of CPD measures knowledge only. 46% measures practice performance. (ACCME 2024)</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # TWO COL - Vicious Cycle (Image LEFT, reverse=False)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": False,
        "alignment": False,
        "width": "third",
        "image_two_col": 3563,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>The Vicious Cycle</strong></span></h1>
<p>Low Engagement = Poor Insights = Can't Prove Value</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>For Members:</strong> Generic library. No guidance on closing THEIR gaps. Complete credits elsewhere.</li>
<li><strong>For Your Board:</strong> Activity metrics only. Can't prove gaps identified or closed. Can't justify investment.</li>
<li><strong>For You:</strong> Low engagement. No insights. Guesswork strategy. Can't demonstrate value.</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Evidence takes 17 years to change practice—but you can't prove you're accelerating that. (JAMA 2023)</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "large"
    })

    # TWO COL - Virtuous Cycle (Image RIGHT, reverse=True)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": 3569,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>The Virtuous Cycle</strong></span></h1>
<p>Gap Identification → Closure Pathways → Better Engagement → Better Insights → More Effective Gap Closure</p>
<p>Yoke creates an integrated system where each element strengthens the others:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Gap Identification:</strong> Members complete brief assessment. Platform identifies clinical knowledge gaps and confidence deficits. You see aggregate insights—which topics show gaps across your membership.</li>
<li><strong>Ability to Close Those Gaps:</strong> Personalized pathways show members "Based on your gaps, complete these modules." Application support with case scenarios, practice tracking, progress visualization. Targeted content creation based on identified gaps.</li>
<li><strong>Better Engagement:</strong> Personalized = relevant. Give-to-get: assessment gives immediate value with personalized dashboard. Members return to track progress and complete certificate pathways.</li>
<li><strong>Better Insights & Proof:</strong> Higher engagement = richer data. Gap-closure tracking shows which modules help members improve. Content performance shows what works and what gaps remain.</li>
<li><strong>More Effective Gap Closure:</strong> Data improves strategy. Better engagement = better outcomes. Proof for board: "Gaps identified, pathways created, engagement increased, improvement tracked."</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Not separate pieces. An integrated system.</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # TWO COL - What You Get (Image LEFT, reverse=False)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": False,
        "alignment": False,
        "width": "third",
        "image_two_col": 3564,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>What You Get</strong></span></h1>
<p>Complete system for outcomes-based CPD that satisfies GMC revalidation and accreditation requirements:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Gap Identification:</strong> Know which topics members struggle with. Aggregate patterns across membership. Personal dashboards for each member.</li>
<li><strong>Ability to Close Gaps:</strong> Personalized pathways. Application support, not just theory. Targeted content strategy.</li>
<li><strong>Better Engagement:</strong> Higher participation (personalized = relevant). Better completion rates. Members return to track progress.</li>
<li><strong>Better Insights & Proof:</strong> Which content works. Gap-closure tracking. Evidence of member improvement.</li>
<li><strong>Better Metrics:</strong> Platform performance improves with engagement. Richer data drives better decisions. Demonstrable value for board and members.</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Better engagement drives better insights, which drives more effective gap closure.</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # TWO COL - 4 Steps (Image RIGHT, reverse=True)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": True,
        "alignment": False,
        "width": "third",
        "image_two_col": 3604,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>4 Steps to Start the Virtuous Cycle</strong></span></h1>
<p>Launch a gap-based CPD system in 2-4 weeks:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>Gap Assessment:</strong> Members identify their clinical knowledge gaps</li>
<li><strong>Personalized Pathways:</strong> Platform recommends content to close those specific gaps</li>
<li><strong>Engagement + Tracking:</strong> Members complete pathways, track progress, apply learning</li>
<li><strong>Insights + Improvement:</strong> You see what works, refine strategy, close more gaps effectively</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Timeline: 2-4 weeks to launch.</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # TWO COL - Why It Works (Image LEFT, reverse=False)
    panels.append({
        "acf_fc_layout": "two_col_panel",
        "reverse": False,
        "alignment": False,
        "width": "third",
        "image_two_col": 894,
        "background_colour": "",
        "border_colour": "",
        "content_two_col": """<h1><span style="color: #003366;"><strong>Why It Works — Built on Research</strong></span></h1>
<p>Yoke addresses the gaps in current CPD approaches:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li><strong>ACCME 2024:</strong> 95% of CPD measures knowledge only. We add gap identification, practice application, and closure tracking.</li>
<li><strong>JAMA 2023:</strong> Evidence takes 17 years to change practice. We identify where members struggle and create targeted pathways to accelerate adoption.</li>
<li><strong>BMC Medical Education 2024:</strong> "Education alone rarely changes practice." We add personalized pathways, application support, and engagement strategies that drive proof.</li>
</ul>
<p>&nbsp;</p>
<h3><span style="color: #003366;"><em>Proven approach backed by peer-reviewed research (2023-2025).</em></span></h3>"""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "medium"
    })

    # SMALL CTA BANNER - Awards
    panels.append({
        "acf_fc_layout": "small_cta_banner",
        "reverse_panel": False,
        "content_type": "nobutton",
        "image_cta_small": 2693,
        "content_cta_small": """<h2><span style="color: #f79801;">Proven Platform</span></h2>
<strong><span style="color: #f79801;">3 MAJOR INDUSTRY AWARDS FOR MEASURABLE IMPACT</span></strong>
<span style="font-weight: 400;">Recognized for innovation in healthcare education and digital communication</span>

<strong><span style="color: #f79801;">10+ PROGRAMS ACROSS 6+ MARKETS</span></strong>
<span style="font-weight: 400;">Deployed globally with proven outcomes measurement</span>

<strong><span style="color: #f79801;">BUILT ON PEER-REVIEWED RESEARCH (2023-2025)</span></strong>
<span style="font-weight: 400;">Evidence-based approach to CPD outcomes and behavior change</span>""",
        "cta_button_small": "",
        "cta_link_small": ""
    })

    # SPACING
    panels.append({
        "acf_fc_layout": "spacing",
        "spacing_size": "large"
    })

    # CONTENT PANEL - Final CTA (LEFT aligned)
    panels.append({
        "acf_fc_layout": "content_panel",
        "alignment": "left",
        "background_colour": False,
        "content_block": """<h1><span style="color: #003366;"><strong>See the Integrated System in Action</strong></span></h1>
<p>Book a 30-minute meeting to see:</p>
<p>&nbsp;</p>
<ul class="custom-ticks yellow">
<li>Gap identification + closure pathways</li>
<li>How personalization drives engagement</li>
<li>Insights dashboard showing what works</li>
<li>How better engagement creates better metrics</li>
</ul>
<p>&nbsp;</p>
<p><a class="button" href="/contact">Book Your 30-Minute Meeting</a></p>"""
    })

    print(f"Created {len(panels)} panels with alternating images")

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

        print("SUCCESS: Page updated with proper layout!")
        print(f"View: https://yokehealth.com/?page_id={page_id}&preview=true")
        print(f"Edit: https://yokehealth.com/wp-admin/post.php?post={page_id}&action=edit")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
