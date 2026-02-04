"""Fix page 4165 status - set to draft so it can be published"""

from wordpress_client import WordPressClient

client = WordPressClient()
page_id = 4165

print("Fixing page status...")

# Just update status to draft
result = client.post(
    f"pages/{page_id}",
    data={
        "status": "draft"
    }
)

print(f"Status now: {result['status']}")
print(f"Modified: {result['modified']}")
print(f"Preview: https://yokehealth.com/?page_id={page_id}&preview=true")
print(f"Edit: https://yokehealth.com/wp-admin/post.php?post={page_id}&action=edit")
print("\nYou should now be able to preview and publish!")
