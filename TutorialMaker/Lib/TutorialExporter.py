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
        """,
        'section': """
            <div class="sectionSlide">
                <div class="sectionContent">
                    <h1 class="sectionTitle">{title}</h1>
                </div>
            </div>
        """,
        'text': """
            <div class="textSlide">
                <div class="textContent">
                    <h2 class="textTitle">{title}</h2>
                    <div class="textBody">{body}</div>
                </div>
            </div>
        """,
        'blank': """
            <div class="blankSlide">
                <div class="blankContent">
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
        """,
        'section': """
            <div class="sectionSlide classic">
                <div class="sectionContent">
                    <div class="coverBorder">
                        <h1 class="sectionTitle">{title}</h1>
                    </div>
                </div>
            </div>
        """,
        'text': """
            <div class="textSlide classic">
                <div class="textContent">
                    <h2 class="textTitle">{title}</h2>
                    <div class="textBody">{body}</div>
                </div>
            </div>
        """,
        'blank': """
            <div class="blankSlide classic">
                <div class="blankContent">
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
        """,
        'section': """
            <div class="sectionSlide minimal">
                <div class="sectionContent">
                    <h1 class="sectionTitle">{title}</h1>
                </div>
            </div>
        """,
        'text': """
            <div class="textSlide minimal">
                <div class="textContent">
                    <h2 class="textTitle">{title}</h2>
                    <div class="textBody">{body}</div>
                </div>
            </div>
        """,
        'blank': """
            <div class="blankSlide minimal">
                <div class="blankContent">
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
''',
        'section': '''
<div style="text-align: center; padding: 60px; background: linear-gradient(135deg, {primary} 0%, {secondary} 100%); color: white; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); margin: 30px auto; max-width: 1200px; min-height: 600px; display: flex; align-items: center; justify-content: center;">

# <span style="font-size: 3.5rem; font-weight: 700; line-height: 1.2; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); display: block;">{title}</span>

</div>

---
''',
        'text': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); padding: 40px;">

## <span style="color: {primary}; font-size: 2.2rem; font-weight: 600; display: block; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 3px solid {primary};">{title}</span>

<div style="font-size: 1.2rem; line-height: 1.8; color: #444; text-align: justify;">

{body}

</div>

</div>

---
''',
        'blank': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; border-radius: 8px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); padding: 40px; min-height: 600px;">

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
''',
        'section': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px; min-height: 600px; display: flex; align-items: center; justify-content: center;">

<div style="border: 3px double {primary}; padding: 60px; text-align: center;">

# <span style="font-size: 3.5rem; font-weight: 700; line-height: 1.3; color: {primary}; font-family: Georgia, serif; display: block;">{title}</span>

</div>

</div>

---
''',
        'text': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px;">

## <span style="color: {primary}; font-size: 2.5rem; font-weight: 600; display: block; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 2px solid {primary}; text-align: center; font-family: Georgia, serif;">{title}</span>

<div style="font-size: 1.15rem; line-height: 1.9; color: {text}; text-align: justify;">

{body}

</div>

</div>

---
''',
        'blank': '''
<div style="background: #fefefe; max-width: 1200px; margin: 30px auto; border: 2px solid {primary}; padding: 50px; min-height: 600px;">

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
''',
        'section': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px; border-left: 8px solid {primary}; min-height: 600px; display: flex; align-items: center; justify-content: center;">

# <span style="font-size: 3.2rem; font-weight: 300; line-height: 1.2; color: {primary}; letter-spacing: -1px; display: block;">{title}</span>

</div>

---
''',
        'text': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px;">

## <span style="color: {primary}; font-size: 2rem; font-weight: 400; display: block; margin-bottom: 30px; padding-bottom: 10px; border-bottom: 1px solid {primary};">{title}</span>

<div style="font-size: 1.1rem; line-height: 1.8; color: {text};">

{body}

</div>

</div>

---
''',
        'blank': '''
<div style="background: white; max-width: 1200px; margin: 30px auto; padding: 60px; min-height: 600px;">

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
        .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
            background: white;
            max-width: 1200px;
            margin: 30px auto;
            border-radius: 8px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
            height: 600px;
            display: flex;
            flex-direction: column;
        }}

        /* Stacked content */
        .slideContent, .textContent, .blankContent {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding: 40px;
        }}

        /* Centered content */
        .coverContent, .backCoverContent, .sectionContent {{
            flex: 0 1 auto;
            min-height: 0;
            overflow: hidden;
            padding: 40px;
        }}

        /* Cover Page */
        .cover {{
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            color: white;
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
            flex-shrink: 0;
            font-size: 2.2rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid {primary};
        }}

        .containerImage {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: #fafafa;
            padding: 10px;
            border-radius: 4px;
        }}

        .slideImage {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        .slideDescription {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #444;
            text-align: justify;
            margin-top: 10px;
        }}

        /* Back Cover */
        .backCover {{
            background: linear-gradient(135deg, {secondary} 0%, {primary} 100%);
            color: white;
            align-items: center;
            justify-content: center;
        }}

        .backCoverContent {{
            max-width: 800px;
            width: 100%;
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

        /* Section Slide */
        .sectionSlide {{
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            color: white;
            align-items: center;
            justify-content: center;
        }}

        .sectionTitle {{
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}

        /* Text Slide */
        .textSlide {{
            background: white;
        }}

        .textTitle {{
            flex-shrink: 0;
            font-size: 2.2rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid {primary};
        }}

        .textBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #444;
            text-align: justify;
        }}

        /* Blank Slide */
        .blankSlide {{
            background: white;
        }}

        .blankBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #444;
        }}

        .slideContent p, .textContent p, .blankContent p {{
            margin: 0 0 0.4em;
        }}

        /* Print Styles */
        @media print {{
            * {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}

            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
                max-width: none;
                width: 297mm;
                height: 148.5mm;
                margin: 0;
                box-shadow: none;
                border-radius: 0;
                overflow: hidden;
            }}

            .slideContent, .textContent, .blankContent {{
                overflow: hidden;
            }}
        }}

        @page {{
            size: 297mm 148.5mm;
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

        .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
            background: #fefefe;
            max-width: 1200px;
            margin: 30px auto;
            border: 2px solid {primary};
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
            height: 600px;
            display: flex;
            flex-direction: column;
        }}

        .slideContent, .textContent, .blankContent {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding: 50px;
        }}

        .coverContent, .backCoverContent, .sectionContent {{
            flex: 0 1 auto;
            min-height: 0;
            overflow: hidden;
            padding: 50px;
        }}

        .cover {{
            background: white;
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
            flex-shrink: 0;
            font-size: 2.5rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid {primary};
            text-align: center;
            font-family: 'Georgia', serif;
        }}

        .containerImage {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 10px;
            border: 1px solid #ddd;
        }}

        .slideImage {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            border: 1px solid {primary};
        }}

        .slideDescription {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
            text-align: justify;
            margin-top: 10px;
        }}

        .backCover {{
            background: white;
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

        /* Section Slide */
        .sectionSlide {{
            background: #fefefe;
            align-items: center;
            justify-content: center;
        }}

        .sectionSlide .coverBorder {{
            border: 3px double {primary};
            padding: 60px;
        }}

        .sectionTitle {{
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.3;
            color: {primary};
            font-family: Georgia, serif;
            text-align: center;
        }}

        /* Text Slide */
        .textSlide {{
            background: #fefefe;
        }}

        .textTitle {{
            flex-shrink: 0;
            font-size: 2.5rem;
            font-weight: 600;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid {primary};
            text-align: center;
            font-family: Georgia, serif;
        }}

        .textBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
            text-align: justify;
        }}

        /* Blank Slide */
        .blankSlide {{
            background: #fefefe;
        }}

        .blankBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
        }}

        .slideContent p, .textContent p, .blankContent p {{
            margin: 0 0 0.4em;
        }}

        @media print {{
            * {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}

            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
                max-width: none;
                width: 297mm;
                height: 148.5mm;
                margin: 0;
                border: none;
                overflow: hidden;
            }}

            .slideContent, .textContent, .blankContent {{
                overflow: hidden;
            }}
        }}

        @page {{
            size: 297mm 148.5mm;
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

        .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
            background: white;
            max-width: 1200px;
            margin: 30px auto;
            overflow: hidden;
            page-break-after: always;
            page-break-inside: avoid;
            height: 600px;
            display: flex;
            flex-direction: column;
        }}
        
        .slideContent, .textContent, .blankContent {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            padding: 60px;
        }}

        .coverContent, .backCoverContent, .sectionContent {{
            flex: 0 1 auto;
            min-height: 0;
            overflow: hidden;
            padding: 60px;
        }}

        .cover {{
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
            flex-shrink: 0;
            font-size: 2rem;
            font-weight: 400;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid {primary};
        }}

        .containerImage {{
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 10px;
        }}

        .slideImage {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
        }}

        .slideDescription {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
            margin-top: 10px;
        }}

        .backCover {{
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

        /* Section Slide */
        .sectionSlide {{
            background: white;
            border-left: 8px solid {primary};
            align-items: center;
            justify-content: center;
        }}

        .sectionTitle {{
            font-size: 3.2rem;
            font-weight: 300;
            line-height: 1.2;
            color: {primary};
            letter-spacing: -1px;
            text-align: center;
        }}

        /* Text Slide */
        .textSlide {{
            background: white;
        }}

        .textTitle {{
            flex-shrink: 0;
            font-size: 2rem;
            font-weight: 400;
            color: {primary};
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid {primary};
        }}

        .textBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
        }}

        /* Blank Slide */
        .blankSlide {{
            background: white;
        }}

        .blankBody {{
            flex-shrink: 1;
            min-height: 0;
            overflow: hidden;
            font-size: 1.1rem;
            line-height: 1.6;
            color: {text};
        }}

        .slideContent p, .textContent p, .blankContent p {{
            margin: 0 0 0.4em;
        }}

        @media print {{
            * {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}

            body {{
                background: white;
                padding: 0;
            }}

            .slide, .cover, .backCover, .sectionSlide, .textSlide, .blankSlide {{
                max-width: none;
                width: 297mm;
                height: 148.5mm;
                margin: 0;
                overflow: hidden;
            }}

            .slideContent, .textContent, .blankContent {{
                overflow: hidden;
            }}
        }}

        @page {{
            size: 297mm 148.5mm;
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
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = HTML_TEMPLATES[theme]['cover']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            author=self.Author,
            date=self.Date,
            description=self.Description,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
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
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
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

    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
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
    def __init__(self, Title: str, Description: str, ImagePath: str, base_dir: str = None):
        self.Title = Title
        self.Description = Description
        self.ImagePath = ImagePath
        self.BaseDir = base_dir
    
    def _get_image_data_url(self, image_path, base_dir: str = None):
        if not image_path:
            return image_path
        if base_dir and not os.path.isabs(image_path):
            image_path = os.path.join(base_dir, image_path)
        if not os.path.exists(image_path):
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
        
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = HTML_TEMPLATES[theme]['slide']
        colors = PALETTE_COLORS[palette]
        base_dir = self.BaseDir
        if embed:
            image_src = self._get_image_data_url(self.ImagePath, base_dir=base_dir)
        else:
            image_src = self.ImagePath or ""

        return template.format(
            title=self.Title,
            image=image_src,
            alt=self.Title,
            description=self.Description,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = MARKDOWN_TEMPLATES[theme]['slide']
        colors = PALETTE_COLORS[palette]
        base_dir = self.BaseDir
        if embed:
            image_src = self._get_image_data_url(self.ImagePath, base_dir=base_dir)
        else:
            image_src = self.ImagePath or ""
        
        return template.format(
            title=self.Title,
            image=image_src,
            alt=self.Title,
            description=self.Description,
            **colors
        )

class SimpleSection():
    def __init__(self, Title: str):
        self.Title = Title
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = HTML_TEMPLATES[theme]['section']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = MARKDOWN_TEMPLATES[theme]['section']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            **colors
        )

class SimpleText():
    def __init__(self, Title: str, Body: str):
        self.Title = Title
        self.Body = Body
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = HTML_TEMPLATES[theme]['text']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            body=self.Body,
            **colors
        )
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = MARKDOWN_TEMPLATES[theme]['text']
        colors = PALETTE_COLORS[palette]
        return template.format(
            title=self.Title,
            body=self.Body,
            **colors
        )

class BlankSlide():
    def __init__(self):
        pass
    
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = HTML_TEMPLATES[theme]['blank']
        colors = PALETTE_COLORS[palette]
        return template.format(**colors)
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        template = MARKDOWN_TEMPLATES[theme]['blank']
        colors = PALETTE_COLORS[palette]
        return template.format(**colors)

# Slide Model and Exporter

class SlideModel():
    Cover= CoverSlide
    SimpleSlide = SimpleSlide
    BackCover = BackCoverSlide
    SimpleSection = SimpleSection
    SimpleText = SimpleText
    Blank = BlankSlide

class SlidePage():
    def __init__(self, Model:SlideModel = SlideModel.SimpleSlide):
        self.Model = Model # Model will be used later to create more than one type of slide

class TutorialExporter():
    def __init__(self, Slides: list[SlidePage], Title: str, html_dir: str = None):
        self.Slides = Slides
        self.Title = Title
        self.HtmlDir = html_dir
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
                        <script>
                        function fitSlides() {{
                            var specs = [
                                {{ container: '.slideContent', texts: ['.slideTitle', '.slideDescription'], scaleUp: false }},
                                {{ container: '.textContent',  texts: ['.textTitle', '.textBody'], scaleUp: true }},
                                {{ container: '.blankContent', texts: ['.blankBody'], scaleUp: true }}
                            ];

                            specs.forEach(function(spec) {{
                                document.querySelectorAll(spec.container).forEach(function(el) {{
                                    var textEls = spec.texts
                                        .map(function(s) {{ return el.querySelector(s); }})
                                        .filter(Boolean);
                                    if (!textEls.length) return;

                                    // reset any previous inline font-size
                                    textEls.forEach(function(t) {{ t.style.fontSize = ''; }});

                                    // Step 1: capture constrained dimensions
                                    var rect      = el.getBoundingClientRect();
                                    var available = rect.height;
                                    var elWidth   = rect.width;
                                    if (available <= 0 || elWidth <= 0) return;

                                    // Step 2: clone off-screen with the SAME width → accurate natural height
                                    function measure(source) {{
                                        var c = source.cloneNode(true);
                                        c.style.cssText = [
                                            'position:fixed',
                                            'top:-99999px',
                                            'left:-99999px',
                                            'width:' + elWidth + 'px',
                                            'height:auto',
                                            'min-height:0',
                                            'overflow:visible',
                                            'flex:none',
                                            'visibility:hidden'
                                        ].join(';');
                                        document.body.appendChild(c);
                                        var h = c.getBoundingClientRect().height;
                                        document.body.removeChild(c);
                                        return h;
                                    }}

                                    var natural = measure(el);

                                    // Step 3: scale UP if text-only slide has significant empty space
                                    if (spec.scaleUp && natural < available * 0.9) {{
                                        var upRatio = (available * 0.95) / natural;
                                        textEls.forEach(function(t) {{
                                            var fs = parseFloat(window.getComputedStyle(t).fontSize);
                                            t.style.fontSize = (fs * upRatio) + 'px';
                                        }});
                                        natural = measure(el);
                                    }}

                                    if (natural <= available) return;

                                    // Step 4: single-shot scale down
                                    var ratio = available / natural;
                                    textEls.forEach(function(t) {{
                                        var fs = parseFloat(window.getComputedStyle(t).fontSize);
                                        t.style.fontSize = Math.max(fs * ratio, 6) + 'px';
                                    }});

                                    // Step 5: one correction pass for line-height rounding
                                    var after = measure(el);
                                    if (after > available) {{
                                        var ratio2 = available / after;
                                        textEls.forEach(function(t) {{
                                            var fs = parseFloat(window.getComputedStyle(t).fontSize);
                                            t.style.fontSize = Math.max(fs * ratio2, 6) + 'px';
                                        }});
                                    }}
                                }});
                            }});
                        }}

                        document.addEventListener('DOMContentLoaded', function() {{
                            requestAnimationFrame(function() {{
                                requestAnimationFrame(fitSlides);
                            }});
                        }});
                        window.addEventListener('beforeprint', fitSlides);
                        </script>
                        </html>
                    """
        self.Markdown = ""
        
    def ToHtml(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        body = "".join([slide.Model.ToHtml(palette=palette, theme=theme, embed=embed) for slide in self.Slides])
        colors = PALETTE_COLORS[palette]
        css = CSS_TEMPLATES[theme].format(**colors)
        return self.Html.format(self.Title, body, css)
    
    def ToMarkdown(self, palette: Palette = Palette.BLUE, theme: Theme = Theme.MODERN, embed: bool = False):
        md = "".join([slide.Model.ToMarkdown(palette=palette, theme=theme, embed=embed) for slide in self.Slides])
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
            doc.setHtml(self.ToHtml(palette=palette, theme=theme, embed=True))
            doc.setPageSize(qt.QSizeF(printer.pageRect().size()))
            doc.print_(printer)
            
            with open(temp_path, 'rb') as f:
                pdf_data = f.read()
            
            return pdf_data
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)