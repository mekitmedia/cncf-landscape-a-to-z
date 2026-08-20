import re

with open("website/themes/cncf-theme/layouts/letters/list.html", "r") as f:
    content = f.read()

# Add filter buttons
filter_buttons_html = """
            {{ if $weekData }}
                <div class="flex flex-wrap gap-2 mb-8 filter-group" aria-label="Filter projects by status">
                    <button class="px-4 py-2 rounded-full text-sm font-medium bg-slate-800 text-white hover:bg-slate-700 transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none filter-btn" data-filter="all" aria-pressed="true">All</button>
                    <button class="px-4 py-2 rounded-full text-sm font-medium bg-slate-200 text-slate-700 hover:bg-slate-300 transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none filter-btn" data-filter="graduated" aria-pressed="false">Graduated</button>
                    <button class="px-4 py-2 rounded-full text-sm font-medium bg-slate-200 text-slate-700 hover:bg-slate-300 transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none filter-btn" data-filter="incubating" aria-pressed="false">Incubating</button>
                    <button class="px-4 py-2 rounded-full text-sm font-medium bg-slate-200 text-slate-700 hover:bg-slate-300 transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none filter-btn" data-filter="sandbox" aria-pressed="false">Sandbox</button>
                </div>
                {{ range $filename, $items := $categoriesData }}
"""

content = content.replace('            {{ if $weekData }}\n                {{ range $filename, $items := $categoriesData }}', filter_buttons_html)

# Add category-section class
content = content.replace('<div class="mb-12">\n                            <h2 class="text-xl font-bold', '<div class="mb-12 category-section">\n                            <h2 class="text-xl font-bold')

# Add project-card class and data-project attribute
card_start = '<div class="bg-white p-6 rounded-2xl border border-slate-200 hover:border-blue-400 hover:shadow-xl hover:shadow-blue-50 transition-all group">'
card_replace = '<div class="bg-white p-6 rounded-2xl border border-slate-200 hover:border-blue-400 hover:shadow-xl hover:shadow-blue-50 transition-all group project-card" data-project="{{ if .project }}{{ lower .project }}{{ else }}none{{ end }}">'
content = content.replace(card_start, card_replace)

# Add JavaScript at the end before </body> or {{ end }}
script = """
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const buttons = document.querySelectorAll(".filter-btn");
        const cards = document.querySelectorAll(".project-card");
        const sections = document.querySelectorAll(".category-section");

        buttons.forEach(button => {
            button.addEventListener("click", () => {
                // Update active button state
                buttons.forEach(btn => {
                    btn.classList.remove("bg-slate-800", "text-white");
                    btn.classList.add("bg-slate-200", "text-slate-700");
                    btn.setAttribute("aria-pressed", "false");
                });
                button.classList.remove("bg-slate-200", "text-slate-700");
                button.classList.add("bg-slate-800", "text-white");
                button.setAttribute("aria-pressed", "true");

                const filter = button.getAttribute("data-filter");

                cards.forEach(card => {
                    if (filter === "all" || card.getAttribute("data-project") === filter) {
                        card.style.display = "";
                    } else {
                        card.style.display = "none";
                    }
                });

                // Hide empty categories
                sections.forEach(section => {
                    let hasVisible = false;
                    section.querySelectorAll('.project-card').forEach(c => {
                        if (c.style.display !== "none") hasVisible = true;
                    });
                    section.style.display = hasVisible ? "" : "none";
                });
            });
        });
    });
</script>
{{ end }}
"""
content = re.sub(r'\{\{\s*end\s*\}\}\s*$', script, content)

with open("website/themes/cncf-theme/layouts/letters/list.html", "w") as f:
    f.write(content)
