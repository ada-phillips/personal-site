import uuid
from PIL import Image, ImageFont, ImageDraw
import flask
from flask import Blueprint, request, send_file

api = Blueprint('api', __name__, url_prefix='/api')

meme_data = {
    "valentia_no_yes": {
        "fields": {
            "0": {
                "max": (1608, 674),
                "min": (791, 0),
                "font": "bitstream_vera_sans/Vera",
                "size_max": 50,
                "size_min": 5,
                "placeholder": "Valentia dislikes"
            },
            "1": {
                "max": (1608, 1381),
                "min": (791, 707),
                "font": "bitstream_vera_sans/Vera",
                "size_max": 50,
                "size_min": 10,
                "placeholder": "Valentia likes"
            }
        },
        "title": "Valentia -- No/Yes"
    }, 
    "valentia_yes_no": {
        "fields": {
            "0": {
                "max": (1608, 674),
                "min": (791, 0),
                "font": "bitstream_vera_sans/Vera",
                "size_max": 50,
                "size_min": 5,
                "placeholder": "Valentia likes"
            },
            "1": {
                "max": (1608, 1381),
                "min": (791, 707),
                "font": "bitstream_vera_sans/Vera",
                "size_max": 50,
                "size_min": 10,
                "placeholder": "Valentia dislikes"
            }
        },
        "title": "Valentia -- Yes/No"
    }
}


@api.route("/meme/<meme_format>")
def meme_gen(meme_format):
    with Image.open("resources/memes/"+meme_format+".png") as template:
        meme_fields = meme_data.get(meme_format, {}).get("fields",{})
        meme = ImageDraw.Draw(template)
        
        for field_name, field_data in meme_fields.items():
            font_file = f"resources/fonts/{field_data.get('font', 'bitstream_vera_sans/Vera')}.ttf"

            font_max = field_data.get("size_max", 20)
            font_min = field_data.get("size_min", 10)
            font_interval = field_data.get("size_interval", 5)

            color = field_data.get("color", (0,0,0))
            text = request.args.get(field_name, "")
            
            max_x, max_y = field_data.get("max", template.size)
            min_x, min_y = field_data.get("min", (0,0))

            field_w = max_x - min_x
            field_h = max_y - min_y


            wrapped_text, font = wrap_text(text, meme, font_file, font_max, font_min, font_interval, field_w, field_h)

            text_w, text_h = meme.textsize(wrapped_text, font=font)

            x = max(min_x, min_x + (field_w - text_w)/2)
            y = max(min_y, min_y + (field_h - text_h)/2)

            meme.text((x, y), wrapped_text, color, font)

        output_file = "meme.png"

        template.save("out/"+output_file, "PNG")
        return flask.send_from_directory("../out", output_file)

def wrap_text(text, image, font_file, font_max, font_min, font_interval, max_width, max_height):
    font = None
    out_text = ""
    for size in range(font_max, font_min-1, -font_interval):
        font = ImageFont.truetype(font=font_file, size=size)
        char_x, char_y = image.textsize(f"M", font=font)

        print(size)

        # quick sanity check that it can fit (or is smallest option)
        if char_x*char_y*len(text) > max_width*max_height and size > font_min:
            continue
        else:
            out_text = ""
            for word in text.split(): 
                text_w, text_h = image.textsize(f"{out_text} {word}", font=font)
                if text_w > max_width:
                    out_text += "\n"
                
                wrapped_w, wrapped_h = image.textsize(f"{out_text} {word}", font=font)

                # If it still can't fit the space, and there's a smaller allowed size, re-run
                if (wrapped_w > max_width or wrapped_h > max_height) and size > font_min:
                    print(f"break size={size}")
                    break
                elif wrapped_h > max_height:
                    print(f"return size={size}")
                    return out_text, font

                out_text += f" {word}"
            else:
                print(f"else size={size}")
                return out_text, font