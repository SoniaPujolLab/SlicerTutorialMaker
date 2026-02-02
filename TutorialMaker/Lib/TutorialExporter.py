import tempfile
import base64
import os
import qt
from enum import Enum

class Palette(Enum):
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    ORANGE = "orange"
    
class Theme(Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    MINIMAL = "minimal"

# Color Definitions

PALETTE_COLORS = {
    Palette.BLUE: {
        'primary': '#003366',
        'secondary': '#004d99',
        'accent': '#0066cc',
        'text': '#333',
        'background': '#f5f5f5'
    },
    Palette.GREEN: {
        'primary': '#1b5e20',
        'secondary': '#2e7d32',
        'accent': '#43a047',
        'text': '#333',
        'background': '#f5f5f5'
    },
    Palette.PURPLE: {
        'primary': '#4a148c',
        'secondary': '#6a1b9a',
        'accent': '#8e24aa',
        'text': '#333',
        'background': '#f5f5f5'
    },
    Palette.ORANGE: {
        'primary': '#e65100',
        'secondary': '#f57c00',
        'accent': '#ff9800',
        'text': '#333',
        'background': '#f5f5f5'
    }
}

# HTML Templates

HTML_TEMPLATES = {
    Theme.MODERN: {
        'cover': """
            <div class="cover">
                <div class="coverContent">
                    <h1 class="coverTitle">{title}</h1>
                    <p class="coverAuthor">By {author}</p>
                    <p class="coverDate">{date}</p>
                    <p class="coverDescription">{description}</p>
                </div>
            </div>
        """,
        'slide': """
            <div class="slide">
                <div class="slideContent">
                    <h2 class="slideTitle">{title}</h2>
                    <div class="containerImage">
                        <img class="slideImage" src="{image}" alt="{alt}">
                    </div>
                    <div class="slideDescription">{description}</div>
                </div>
            </div>
        """,
        'backcover': """
            <div class="backCover">
                <div class="backCoverContent">
                    <h1 class="coverTitle">{title}</h1>
                    <ul class="coverAcknowledgments">
                        {items}
                    </ul>
                </div>
            </div>
        """
    },
    Theme.CLASSIC: {
        'cover': """
            <div class="cover classic">
                <div class="coverContent">
                    <div class="coverBorder">
                        <h1 class="coverTitle">{title}</h1>
                        <p class="coverAuthor">By {author}</p>
                        <p class="coverDate">{date}</p>
                        <p class="coverDescription">{description}</p>
                    </div>
                </div>
            </div>
        """,
        'slide': """
            <div class="slide classic">
                <div class="slideContent">
                    <h2 class="slideTitle">{title}</h2>
                    <div class="containerImage">
                        <img class="slideImage" src="{image}" alt="{alt}">
                    </div>
                    <div class="slideDescription">{description}</div>
                </div>
            </div>
        """,
        'backcover': """
            <div class="backCover classic">
                <div class="backCoverContent">
                    <div class="coverBorder">
                        <h1 class="coverTitle">{title}</h1>
                        <ul class="coverAcknowledgments">
                            {items}
                        </ul>
                    </div>
                </div>
            </div>
        """
    },
    Theme.MINIMAL: {
        'cover': """
            <div class="cover minimal">
                <div class="coverContent">
                    <h1 class="coverTitle">{title}</h1>
                    <p class="coverAuthor">{author}</p>
                    <p class="coverDate">{date}</p>
                    <p class="coverDescription">{description}</p>
                </div>
            </div>
        """,
        'slide': """
            <div class="slide minimal">
                <div class="slideContent">
                    <h2 class="slideTitle">{title}</h2>
                    <div class="containerImage">
                        <img class="slideImage" src="{image}" alt="{alt}">
                    </div>
                    <div class="slideDescription">{description}</div>
                </div>
            </div>
        """,
        'backcover': """
            <div class="backCover minimal">
                <div class="backCoverContent">
                    <h1 class="coverTitle">{title}</h1>
                    <ul class="coverAcknowledgments">
                        {items}
                    </ul>
                </div>
            </div>
        """
    }
}

# Markdown Templates

MARKDOWN_TEMPLATES = {
    Theme.MODERN: {
        'cover': '''
<div style="text-align: center; padding: 60px; background: linear-gradient(135deg, {primary} 0%, {secondary} 100%); color: white; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); margin: 30px auto; max-width: 1200px; min-height: 600px; display: flex; flex-direction: column; align-items: center; justify-content: center;">

<div style="max-width: 800px;">

# <span style="font-size: 3.5rem; font-weight: 700; margin-bottom: 30px; line-height: 1.2; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); display: block;">{title}</span>

<p style="font-size: 1.5rem; font-weight: 300; margin-bottom: 15px; opacity: 0.95;">By {author}</p>

<p style="font-size: 1.2rem; font-weight: 300; margin-bottom: 40px; opacity: 0.85;">{date}</p>

<p style="font-size: 1.3rem; line-height: 1.8; font-weight: 300; opacity: 0.9; max-width: 700px; margin: 0 auto;">{description}</p>

</div>

</div>

---
''',
        'slide': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); padding: 40px;">

## <span style="color: {primary}; font-size: 2.2rem; font-weight: 600; display: block; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 3px solid {primary};">{title}</span>

<div style="text-align: center; margin: 30px 0; background: #fafafa; padding: 20px; border-radius: 4px;">

![{alt}]({image})

</div>

<div style="font-size: 1.2rem; line-height: 1.8; color: #444; text-align: justify; margin-top: 25px;">

{description}

</div>

</div>

---
''',
        'backcover': '''
<div style="text-align: center; padding: 40px; background: linear-gradient(135deg, {secondary} 0%, {primary} 100%); color: white; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); margin: 30px auto; max-width: 1200px; min-height: 600px; display: flex; flex-direction: column; align-items: center; justify-content: center;">

<div style="max-width: 800px;">

# <span style="font-size: 2.8rem; margin-bottom: 40px; display: block; border-bottom: 2px solid rgba(255, 255, 255, 0.3); padding-bottom: 20px;">{title}</span>

<div style="text-align: left;">

{items}

</div>

</div>

</div>

---
'''
    },
    Theme.CLASSIC: {
        'cover': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px; min-height: 600px; display: flex; align-items: center; justify-content: center;">

<div style="border: 3px double {primary}; padding: 60px; text-align: center;">

# <span style="font-size: 3.5rem; font-weight: 700; margin-bottom: 30px; line-height: 1.3; color: {primary}; font-family: Georgia, serif; display: block;">{title}</span>

<p style="font-size: 1.4rem; margin-bottom: 15px; color: {text}; font-style: italic;">By {author}</p>

<p style="font-size: 1.1rem; margin-bottom: 40px; color: {text};">{date}</p>

<p style="font-size: 1.2rem; line-height: 1.9; color: {text}; max-width: 700px; margin: 0 auto;">{description}</p>

</div>

</div>

---
''',
        'slide': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px;">

## <span style="color: {primary}; font-size: 2.5rem; font-weight: 600; display: block; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 2px solid {primary}; text-align: center; font-family: Georgia, serif;">{title}</span>

<div style="text-align: center; margin: 30px 0; padding: 20px; border: 1px solid #ddd;">

![{alt}]({image})

</div>

<div style="font-size: 1.15rem; line-height: 1.9; color: {text}; text-align: justify; margin-top: 25px;">

{description}

</div>

</div>

---
''',
        'backcover': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px; min-height: 600px; display: flex; align-items: center; justify-content: center;">

<div style="border: 3px double {primary}; padding: 60px; text-align: center;">

# <span style="font-size: 2.5rem; margin-bottom: 40px; color: {primary}; display: block;">{title}</span>

<div style="text-align: left;">

{items}

</div>

</div>

</div>

---
'''
    },
    Theme.MINIMAL: {
        'cover': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px; border-left: 8px solid {primary}; min-height: 600px; display: flex; align-items: center; justify-content: center;">

<div>

# <span style="font-size: 3.2rem; font-weight: 300; margin-bottom: 30px; line-height: 1.2; color: {primary}; letter-spacing: -1px; display: block;">{title}</span>

<p style="font-size: 1.3rem; font-weight: 300; margin-bottom: 15px; color: {text};">{author}</p>

<p style="font-size: 1rem; margin-bottom: 40px; color: #666;">{date}</p>

<p style="font-size: 1.1rem; line-height: 1.7; color: {text}; max-width: 700px;">{description}</p>

</div>

</div>

---
''',
        'slide': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px;">

## <span style="color: {primary}; font-size: 2rem; font-weight: 400; display: block; margin-bottom: 30px; padding-bottom: 10px; border-bottom: 1px solid {primary};">{title}</span>

<div style="text-align: center; margin: 30px 0;">

![{alt}]({image})

</div>

<div style="font-size: 1.1rem; line-height: 1.8; color: {text}; margin-top: 25px;">

{description}

</div>

</div>

---
''',
        'backcover': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px; border-left: 8px solid {primary}; min-height: 600px; display: flex; align-items: center; justify-content: center;">

<div>

# <span style="font-size: 2.5rem; margin-bottom: 40px; color: {primary}; display: block;">{title}</span>

<div style="text-align: left;">

{items}

</div>

</div>

</div>

---
'''
    }
}

# CSS Templates

CSS_TEMPLATES = {
    Theme.MODERN: """
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: {text};
            background: {background};
            padding: 20px;
        }}

        /* Slide Containers */
        .slide, .cover, .backCover {{
            background: white;
            max-width: 1200px;
            margin: 30px auto;
            border-radius: 8px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
        }}

        /* Content Wrappers */
        .slideContent, .coverContent, .backCoverContent {{
            padding: 40px;
        }}

        /* Cover Page */
        .cover {{
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            color: white;
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .coverContent {{
            text-align: center;
            max-width: 800px;
        }}

        .coverTitle {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 30px;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .coverAuthor {{
            font-size: 1.5rem;
            font-weight: 300;
            margin-bottom: 15px;
            opacity: 0.95;
        }}

        .coverDate {{
            font-size: 1.2rem;
            font-weight: 300;
            margin-bottom: 40px;
            opacity: 0.85;
        }}

        .coverDescription {{
            font-size: 1.3rem;
            line-height: 1.8;
            font-weight: 300;
            opacity: 0.9;
            max-width: 700px;
            margin: 0 auto;
        }}

        /* Regular Slides */
        .slideTitle {{
            font-size: 2.2rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid {primary};
        }}

        .containerImage {{
            text-align: center;
            margin: 30px 0;
            background: #fafafa;
            padding: 20px;
            border-radius: 4px;
        }}

        .slideImage {{
            max-width: 90%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        .slideDescription {{
            font-size: 1.2rem;
            line-height: 1.8;
            color: #444;
            text-align: justify;
            margin-top: 25px;
        }}

        /* Back Cover */
        .backCover {{
            background: linear-gradient(135deg, {secondary} 0%, {primary} 100%);
            color: white;
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .backCoverContent {{
            max-width: 800px;
        }}

        .backCover .coverTitle {{
            font-size: 2.8rem;
            margin-bottom: 40px;
            text-align: center;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 20px;
        }}

        .coverAcknowledgments {{
            list-style: none;
            padding: 0;
        }}

        .coverAcknowledgments li {{
            margin-bottom: 25px;
        }}

        .ackItem {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid rgba(255, 255, 255, 0.5);
        }}

        .ackItem strong {{
            display: block;
            font-size: 1.4rem;
            margin-bottom: 10px;
            color: #fff;
        }}

        .ackItem p {{
            font-size: 1.1rem;
            line-height: 1.6;
            opacity: 0.9;
            margin: 0;
        }}

        /* Print Styles */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover {{
                margin: 0;
                box-shadow: none;
                border-radius: 0;
                min-height: 100vh;
                height: auto;
            }}
        }}

        @page {{
            size: A4 landscape;
            margin: 0;
        }}
    """,
    Theme.CLASSIC: """
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: {text};
            background: {background};
            padding: 20px;
        }}

        .slide, .cover, .backCover {{
            background: #fefefe;
            max-width: 1200px;
            margin: 30px auto;
            border: 2px solid {primary};
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
        }}

        .slideContent, .coverContent, .backCoverContent {{
            padding: 50px;
        }}

        .cover {{
            background: white;
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .coverBorder {{
            border: 3px double {primary};
            padding: 60px;
            text-align: center;
        }}

        .coverTitle {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 30px;
            line-height: 1.3;
            color: {primary};
            font-family: 'Georgia', serif;
        }}

        .coverAuthor {{
            font-size: 1.4rem;
            margin-bottom: 15px;
            color: {text};
            font-style: italic;
        }}

        .coverDate {{
            font-size: 1.1rem;
            margin-bottom: 40px;
            color: {text};
        }}

        .coverDescription {{
            font-size: 1.2rem;
            line-height: 1.9;
            color: {text};
            max-width: 700px;
            margin: 0 auto;
        }}

        .slideTitle {{
            font-size: 2.5rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid {primary};
            text-align: center;
            font-family: 'Georgia', serif;
        }}

        .containerImage {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
        }}

        .slideImage {{
            max-width: 85%;
            height: auto;
            border: 1px solid {primary};
        }}

        .slideDescription {{
            font-size: 1.15rem;
            line-height: 1.9;
            color: {text};
            text-align: justify;
            margin-top: 25px;
        }}

        .backCover {{
            background: white;
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .backCover .coverTitle {{
            font-size: 2.5rem;
            margin-bottom: 40px;
            text-align: center;
            color: {primary};
        }}

        .coverAcknowledgments {{
            list-style: none;
            padding: 0;
        }}

        .coverAcknowledgments li {{
            margin-bottom: 25px;
        }}

        .ackItem {{
            background: #fafafa;
            padding: 20px;
            border-left: 4px solid {primary};
            color: {text};
        }}

        .ackItem strong {{
            display: block;
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: {primary};
        }}

        .ackItem p {{
            font-size: 1.1rem;
            line-height: 1.7;
            margin: 0;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover {{
                margin: 0;
                border: none;
                min-height: 100vh;
                height: auto;
            }}
        }}

        @page {{
            size: A4 landscape;
            margin: 0;
        }}
    """,
    Theme.MINIMAL: """
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: {text};
            background: white;
            padding: 20px;
        }}

        .slide, .cover, .backCover {{
            background: white;
            max-width: 1200px;
            margin: 30px auto;
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
        }}

        .slideContent, .coverContent, .backCoverContent {{
            padding: 60px;
        }}

        .cover {{
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-left: 8px solid {primary};
        }}

        .coverTitle {{
            font-size: 3.2rem;
            font-weight: 300;
            margin-bottom: 30px;
            line-height: 1.2;
            color: {primary};
            letter-spacing: -1px;
        }}

        .coverAuthor {{
            font-size: 1.3rem;
            font-weight: 300;
            margin-bottom: 15px;
            color: {text};
        }}

        .coverDate {{
            font-size: 1rem;
            margin-bottom: 40px;
            color: #666;
        }}

        .coverDescription {{
            font-size: 1.1rem;
            line-height: 1.7;
            color: {text};
            max-width: 700px;
        }}

        .slideTitle {{
            font-size: 2rem;
            font-weight: 400;
            color: {primary};
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 1px solid {primary};
        }}

        .containerImage {{
            text-align: center;
            margin: 30px 0;
        }}

        .slideImage {{
            max-width: 100%;
            height: auto;
        }}

        .slideDescription {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: {text};
            margin-top: 25px;
        }}

        .backCover {{
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-left: 8px solid {primary};
        }}

        .backCover .coverTitle {{
            font-size: 2.5rem;
            margin-bottom: 40px;
            color: {primary};
        }}

        .coverAcknowledgments {{
            list-style: none;
            padding: 0;
        }}

        .coverAcknowledgments li {{
            margin-bottom: 20px;
        }}

        .ackItem {{
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }}

        .ackItem strong {{
            display: block;
            font-size: 1.2rem;
            margin-bottom: 8px;
            color: {primary};
            font-weight: 500;
        }}

        .ackItem p {{
            font-size: 1rem;
            line-height: 1.6;
            color: {text};
            margin: 0;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover {{
                margin: 0;
                min-height: 100vh;
                height: auto;
            }}
        }}

        @page {{
            size: A4 landscape;
            margin: 0;
        }}
    """
}

# Slide Classes

class CoverSlide():
    def __init__(self, title: str, author: str, date: str, description: str):
        self.Title = title
        self.Author = author
        self.Date = date
        self.Description = description
        pass
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        template = HTML_TEMPLATES[theme]['cover']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            author=self.Author,
            date=self.Date,
            description=self.Description,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        template = MARKDOWN_TEMPLATES[theme]['cover']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            author=self.Author,
            date=self.Date,
            description=self.Description,
            **colors
        )

class BackCoverSlide():
    def __init__(self, title: str, Acknowledgments: str):
        self.Title = title
        self.Acknowledgments = Acknowledgments 
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        if isinstance(self.Acknowledgments, dict):
            items = "".join(
                f"<li><div class='ackItem'><strong>{k}</strong><p>{v}</p></div></li>"
                for k, v in self.Acknowledgments.items()
            )
        else:
            text = (self.Acknowledgments or "").strip()
            items = f"<li><div class='ackItem'>{text}</div></li>" if text else ""

        template = HTML_TEMPLATES[theme]['backcover']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            items=items,
            **colors
        )

    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        colors = PALETTE_COLORS[palette]
        
        if isinstance(self.Acknowledgments, dict):
            # Create styled acknowledgment items matching HTML structure
            if theme == Theme.MODERN:
                items = "\n\n".join(
                    f'<div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 6px; border-left: 4px solid rgba(255, 255, 255, 0.5); margin-bottom: 25px;">\n\n**<span style="font-size: 1.4rem; display: block; margin-bottom: 10px; color: #fff;">{k}</span>**\n\n<p style="font-size: 1.1rem; line-height: 1.6; opacity: 0.9; margin: 0;">{v}</p>\n\n</div>'
                    for k, v in self.Acknowledgments.items()
                )
            elif theme == Theme.CLASSIC:
                items = "\n\n".join(
                    f'<div style="background: #fafafa; padding: 20px; border-left: 4px solid {colors["primary"]}; color: {colors["text"]}; margin-bottom: 25px;">\n\n**<span style="font-size: 1.3rem; display: block; margin-bottom: 10px; color: {colors["primary"]};">{k}</span>**\n\n<p style="font-size: 1.1rem; line-height: 1.7; margin: 0;">{v}</p>\n\n</div>'
                    for k, v in self.Acknowledgments.items()
                )
            else:  # MINIMAL
                items = "\n\n".join(
                    f'<div style="padding: 15px 0; border-bottom: 1px solid #eee; margin-bottom: 20px;">\n\n**<span style="font-size: 1.2rem; display: block; margin-bottom: 8px; color: {colors["primary"]}; font-weight: 500;">{k}</span>**\n\n<p style="font-size: 1rem; line-height: 1.6; color: {colors["text"]}; margin: 0;">{v}</p>\n\n</div>'
                    for k, v in self.Acknowledgments.items()
                )
        else:
            text = (self.Acknowledgments or "").strip()
            items = text if text else ""

        template = MARKDOWN_TEMPLATES[theme]['backcover']
        return template.format(
            title=self.Title,
            items=items,
            **colors
        )

class SimpleSlide():
    def __init__(self, Title: str, Description: str, ImagePath: str):
        self.Title = Title
        self.Description = Description
        self.ImagePath = ImagePath
    
    def _get_image_data_url(self, image_path):
        if not image_path or not os.path.exists(image_path):
            return image_path
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                
            ext = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.svg': 'image/svg+xml'
            }
            mime_type = mime_types.get(ext, 'image/png')
            b64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{b64_data}"
        
        except Exception as e:
            print(f"Warning: Could not convert image to base64 ({image_path}): {e}")
            return image_path
        
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        template = HTML_TEMPLATES[theme]['slide']
        colors = PALETTE_COLORS[palette]
        
        image_src = self._get_image_data_url(self.ImagePath)

        return template.format(
            title=self.Title,
            image=image_src,
            alt=self.Title,
            description=self.Description,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        template = MARKDOWN_TEMPLATES[theme]['slide']
        colors = PALETTE_COLORS[palette]
        
        image_src = self._get_image_data_url(self.ImagePath)
        
        return template.format(
            title=self.Title,
            image=image_src,
            alt=self.Title,
            description=self.Description,
            **colors
        )

class SlideModel():
    Cover= CoverSlide
    SimpleSlide = SimpleSlide
    BackCover = BackCoverSlide

class SlidePage():
    def __init__(self, Model:SlideModel = SlideModel.SimpleSlide):
        self.Model = Model # Model will be used later to create more than one type of slide

class TutorialExporter():
    def __init__(self, Slides: list[SlidePage], Title: str):
        self.Slides = Slides
        self.Title = Title
        self.Html = """ <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{}</title>
                        </head>
                        <body>
                            {}
                        </body>
                        <style>
                            {}
                        </style>
                        </html>
                    """
        self.Markdown = ""
        
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        body = "".join([slide.Model.ToHtml(palette=palette, theme=theme) for slide in self.Slides])
        colors = PALETTE_COLORS[palette]
        css = CSS_TEMPLATES[theme].format(**colors)
        return self.Html.format(self.Title, body, css)
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        md = "".join([slide.Model.ToMarkdown(palette=palette, theme=theme) for slide in self.Slides])
        self.Markdown = md
        return md
    
    def ToPdf(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN):
        fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        try:
            printer = qt.QPrinter(qt.QPrinter.PrinterResolution)
            printer.setOutputFormat(qt.QPrinter.PdfFormat)
            printer.setOutputFileName(temp_path)
            printer.setPaperSize(qt.QPageSize.A4)
            printer.setOrientation(qt.QPrinter.Landscape)

            doc = qt.QTextDocument()
            doc.setHtml(self.ToHtml(palette=palette, theme=theme))
            doc.setPageSize(qt.QSizeF(printer.pageRect().size()))
            doc.print_(printer)
            
            with open(temp_path, 'rb') as f:
                pdf_data = f.read()
            
            return pdf_data
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)