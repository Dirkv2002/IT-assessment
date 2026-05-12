# ---------------- SETTINGS ----------------
base_width = 120
base_height = 50
gap = 2
laneX = 140

colors = ["#add8e6", "#90ee90", "#ffa07a", "#f0e68c", "#dda0dd"]

folder_names = [
    "Projects", "Important Reports", "Images and Photos",
    "Video Files Collection", "Archives", "Draft Documents",
    "Invoices 2026", "Presentations for Clients", "Meeting Notes",
    "Miscellaneous Stuff", "Teams phone", "Dynamic 365",
    "Exclaimer", "Facilities management", "BEE",
    "Intranet content", "Multimedia", "Internal audit",
    "Journals", "Procurement", "VAT report",
    "Event photos", "Building drawings", "Valuations",
    "Risk and compliance", "Social housing Act", "Fraud policy",
    "Basic conditions of Employment Act", "Communicare logo",
]

folder_divs = "".join([f'<div class="folder">{n}</div>' for n in folder_names])

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Interactive Folder Workbook</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

<style>
body {{
    margin: 0;
    font-family: "Segoe UI", Arial, sans-serif;
    background: #f7fbff;
    min-height: 120vh;
    overflow-x: hidden;
}}

#instructions {{
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 720px;
    background: rgba(0, 174, 239, 0.92);
    color: white;
    border-radius: 14px;
    padding: 16px 20px;
    z-index: 9999;
}}

.folder {{
    position:absolute;
    width:{base_width}px;
    min-height:{base_height}px;
    padding: 7px;
    border-radius: 10px;
    background: #fff;
    border: 1px solid #d0d7e2;
    cursor: grab;
    text-align:center;
}}

#submitBtn {{
    position: fixed;
    top: 14px;
    right: 16px;
    z-index: 9999;
    padding: 10px 16px;
    border-radius: 10px;
    background: #007aa6;
    color: white;
    border: none;
}}

#candidateName {{
    position: fixed;
    top: 14px;
    left: 16px;
    z-index: 9999;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
}}
</style>
</head>

<body>

<!-- ✅ NAME INPUT -->
<input id="candidateName" type="text" placeholder="Enter your full name">

<div id="instructions">
    <h2>Folder Organisation Exercise</h2>
    <p>Drag folders and organise them logically.</p>
</div>

<button id="submitBtn">Submit & Download PDF</button>

<div id="container" style="position:relative;">
    {folder_divs}
</div>

<script>
let folders = document.querySelectorAll('.folder');

/* ================= NAME STORAGE ================= */
let candidateName = "";

document.getElementById("candidateName").addEventListener("input", function(e) {{
    candidateName = e.target.value;
}});

/* ================= ORIGINAL SYSTEM (UNCHANGED) ================= */
const rootX = 20;
const laneX = {laneX};
const gap = {gap};
const colors = {colors};

folders.forEach(f => {{
    f.childrenList = [];
    f.parentFolder = null;
}});

let rootFolders = Array.from(folders);

function getSubtreeHeight(node) {{
    if (node.childrenList.length === 0) {{
        return node.offsetHeight + gap;
    }}

    let h = 0;
    node.childrenList.forEach(child => {{
        h += getSubtreeHeight(child);
    }});

    return Math.max(h, node.offsetHeight + gap);
}}

function layout(node, level, x, y) {{
    node.dataset.level = level;
    node.style.left = x + "px";
    node.style.top = y + "px";
    node.style.backgroundColor = colors[level % colors.length];

    let currentY = y;

    node.childrenList.forEach(child => {{
        let h = getSubtreeHeight(child);
        layout(child, level + 1, x + laneX, currentY);
        currentY += h;
    }});
}}

function layoutAll() {{
    let y = 200;

    rootFolders.forEach(root => {{
        let h = getSubtreeHeight(root);
        layout(root, 0, rootX, y);
        y += h;
    }});
}}

folders.forEach(folder => {{

    folder.onmousedown = function(e) {{
        let shiftX = e.clientX - folder.getBoundingClientRect().left;
        let shiftY = e.clientY - folder.getBoundingClientRect().top;

        function moveAt(x, y) {{
            folder.style.left = x - shiftX + "px";
            folder.style.top = y - shiftY + "px";
        }}

        function onMove(e) {{
            moveAt(e.pageX, e.pageY);
        }}

        document.addEventListener('mousemove', onMove);

        document.onmouseup = function() {{
            document.removeEventListener('mousemove', onMove);
            document.onmouseup = null;
        }};
    }};

    folder.ondragstart = () => false;
}});

layoutAll();

/* ================= SUBMIT ================= */
document.getElementById("submitBtn").onclick = function () {{

    const now = new Date();

    const formatted =
        now.getFullYear() + "-" +
        String(now.getMonth() + 1).padStart(2, '0') + "-" +
        String(now.getDate()).padStart(2, '0') + " " +
        String(now.getHours()).padStart(2, '0') + ":" +
        String(now.getMinutes()).padStart(2, '0');

    const element = document.body;

    const opt = {{
        margin: 0.3,
        filename: 'ITIB_assessment.pdf',
        image: {{ type: 'jpeg', quality: 0.98 }},
        html2canvas: {{ scale: 2 }},
        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'landscape' }}
    }};

    html2pdf()
        .set(opt)
        .from(element)
        .outputPdf('datauristring')
        .then(function(pdfBase64) {{

            fetch("/submit_pdf", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    name: candidateName,
                    pdf: pdfBase64,
                    timeLeft: "N/A"
                }})
            }});

        }});
}};
</script>

</body>
</html>
"""

file_path = r"C:\Users\dvermeulen\Desktop\assessment.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("ITIB assessment generated:", file_path)