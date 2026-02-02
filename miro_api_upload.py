import requests
import os
import json

def main():
    print("="*70)
    print("MIRO API - CREATE BOARD AND UPLOAD IMAGE")
    print("="*70)

    # OAuth access token
    access_token = "eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_a72WTns-0AuubvXqiSenP7chjMY"

    screenshot_name = "hex_co_homepage.png"
    screenshot_path = os.path.abspath(screenshot_name)

    if not os.path.exists(screenshot_name):
        print(f"\nERROR: Screenshot not found: {screenshot_path}")
        return

    print(f"\nScreenshot ready: {screenshot_name}")

    # Miro API base URL
    api_base = "https://api.miro.com/v2"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    # Step 1: Create a new board
    print("\nStep 1: Creating new board...")
    board_data = {
        "name": "test for home screen",
        "policy": {
            "permissionsPolicy": {
                "collaborationToolsStartAccess": "all_editors",
                "copyAccess": "anyone",
                "sharingAccess": "team_members_with_editing_rights"
            },
            "sharingPolicy": {
                "access": "private",
                "inviteToAccountAndBoardLinkAccess": "no_access",
                "organizationAccess": "private",
                "teamAccess": "private"
            }
        }
    }

    try:
        response = requests.post(
            f"{api_base}/boards",
            headers=headers,
            json=board_data
        )

        if response.status_code == 201:
            board = response.json()
            board_id = board['id']
            board_url = board['viewLink']
            print(f"Board created successfully!")
            print(f"Board ID: {board_id}")
            print(f"Board URL: {board_url}")
        else:
            print(f"Failed to create board: {response.status_code}")
            print(f"Response: {response.text}")
            return

    except Exception as e:
        print(f"Error creating board: {str(e)}")
        return

    # Step 2: Upload image to board
    print("\nStep 2: Uploading hex.co screenshot to board...")

    try:
        # Upload image file
        with open(screenshot_path, 'rb') as f:
            files = {
                'resource': (screenshot_name, f, 'image/png')
            }

            upload_headers = {
                "Authorization": f"Bearer {access_token}"
            }

            # Upload image to board
            upload_response = requests.post(
                f"{api_base}/boards/{board_id}/images",
                headers=upload_headers,
                files=files,
                data={
                    'position': json.dumps({'x': 0, 'y': 0}),
                    'geometry': json.dumps({'width': 800})
                }
            )

            if upload_response.status_code == 201:
                image_data = upload_response.json()
                print("Image uploaded successfully!")
                print(f"Image ID: {image_data.get('id', 'N/A')}")
            else:
                print(f"Failed to upload image: {upload_response.status_code}")
                print(f"Response: {upload_response.text}")

    except Exception as e:
        print(f"Error uploading image: {str(e)}")

    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print(f"\nBoard Name: test for home screen")
    print(f"Board URL: {board_url}")
    print("Screenshot: hex.co homepage")

    # Clean up
    if os.path.exists(screenshot_name):
        os.remove(screenshot_name)
        print(f"\nCleaned up temp file: {screenshot_name}")

if __name__ == "__main__":
    main()
