function fetchStudents() {
    fetch('/students')
        .then(response => response.json())
        .then(students => {
            const tbody = document.querySelector('#student-table tbody');
            tbody.innerHTML = '';
            students.forEach(student => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.grade}</td>
                    <td class="actions">
                        <button class="edit" onclick="editStudent(${student.id})">Edit</button>
                        <button class="delete" onclick="deleteStudent(${student.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function addStudent() {
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const grade = document.getElementById('grade').value;

    fetch('/students', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, age, grade })
    }).then(() => fetchStudents());
}

function deleteStudent(id) {
    fetch(`/students/${id}`, { method: 'DELETE' }).then(() => fetchStudents());
}

window.onload = fetchStudents;
