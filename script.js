document.getElementById("donor-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById("donor-name").value,
        age: document.getElementById("donor-age").value,
        blood_group: document.getElementById("donor-blood-group").value,
        organ: document.getElementById("donor-organ").value,
        location: document.getElementById("donor-location").value,
    };
    const response = await fetch("/add_donor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    alert((await response.json()).message);
});

document.getElementById("recipient-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById("recipient-name").value,
        age: document.getElementById("recipient-age").value,
        blood_group: document.getElementById("recipient-blood-group").value,
        organ_required: document.getElementById("recipient-organ").value,
        location: document.getElementById("recipient-location").value,
        priority: document.getElementById("recipient-priority").value,
    };
    const response = await fetch("/add_recipient", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    alert((await response.json()).message);
});

document.getElementById("match-btn").addEventListener("click", async () => {
    const response = await fetch("/match_organ");
    const matches = await response.json();
    const resultsDiv = document.getElementById("match-results");
    resultsDiv.innerHTML = matches.length
        ? matches.map(
              (m) =>
                  <p>Recipient: ${m[0]} (Organ: ${m[1]}, Blood Group: ${m[2]}) - Donor: ${m[3]}</p>
          ).join("")
        : "<p>No matches found.</p>";
});