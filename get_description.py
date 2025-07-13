from bs4 import BeautifulSoup


def extract_flexible_job_description(html):
    # soup = BeautifulSoup(html, 'html.parser')
    container = html.find("div", class_="styles_JDC__dang-inner-html__h0K4t")
    if not container:
        return {}

    sections = {}
    current_section = "General Description"
    sections[current_section] = ""  

    for child in container.children:
        if not hasattr(child, "get_text"):
            continue

        # Detect section headings
        if child.name in ["div", "b"]:
            heading = child.get_text(strip=True)
            if heading and len(heading) < 100:
                current_section = heading
                if current_section not in sections:
                    sections[current_section] = ""
                continue

        # Collect content under the current section
        if child.name in ["div", "ul", "p"]:
            content = child.get_text(separator="\n", strip=True)
            if content:
                sections[current_section] += "\n" + content

    # Clean up whitespace
    sections = {k: v.strip() for k, v in sections.items() if v.strip()}
    # print(sections)
    return sections
