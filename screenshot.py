from PIL import Image, ImageDraw, ImageFont

# Config
screenshot_dir = "screenshots"
screen_width = 400
buffer_height = 10  # Additional buffer height
import os

def make_image(file_name, text, text_color, outline_color, text_size, line_spacing = 0):
    # Set initial height to 1
    image = Image.new("RGBA", (screen_width, 1), (0, 0, 0, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Choose a font and size (replace 'font_path' with the path to your desired font file)
    font_path = "baloo/Baloo-Regular.ttf"
    font = ImageFont.truetype(font_path, text_size)

    # Calculate text position and set maximum width for multiline text
    max_text_width = screen_width - 20
    text_position = (10, 0)  # Start at the top
    line_height = font.getsize('hg')[1] + line_spacing  # Adjust the line height based on font metrics

    # Draw multiline text on the image and dynamically adjust height
    lines, words = [], text.split()
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        test_width, _ = draw.textsize(test_line, font)

        if test_width <= max_text_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    # Calculate total text height including buffer
    total_text_height = len(lines) * line_height

    # Resize the image based on the calculated text height and add buffer
    image = image.resize((screen_width, int(total_text_height) + 5))  # Adding buffer (5) for the last line
    draw = ImageDraw.Draw(image)


    # Draw text with outlines
    # Draw text with outlines
    for line in lines:
        # Draw text with thicker outline
        for i in range(-2, 3):
            for j in range(-2, 3):
                draw.text((text_position[0] + i, text_position[1] + j), line, font=font, fill=outline_color)
        draw.text(text_position, line, font=font, fill=text_color)  # Draw the text itself
        text_position = (text_position[0], text_position[1] + line_height)  # Adjust Y position for the next line

    # Save the image
    image.save(file_name)



def getPostScreenshots(file_prefix, script):
    os.makedirs(screenshot_dir, exist_ok=True)
    # GET TITLE:
    post_title = script.title
    title_filename = f"{screenshot_dir}/{file_prefix}-Post.png"
    make_image(title_filename, post_title, "white", "black", 40)
    script.titleSCFile = title_filename

    for script_frame in script.frames:
        comment_text = script_frame.text
        comment_id = script_frame.commentId
        comment_filename = f"{screenshot_dir}/{file_prefix}-{comment_id}.png"
        make_image(comment_filename, comment_text, "white", "black", 35)
        script_frame.screenShotFile = comment_filename
