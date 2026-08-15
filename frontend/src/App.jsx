
import { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskPriority, setTaskPriority] = useState("medium");
  const [taskDueDate, setTaskDueDate] = useState("");
  const [taskProjectId, setTaskProjectId] = useState("");
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("Logging in...");

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("access_token", data.access_token);

      setLoggedIn(true);
      setMessage("");

      loadProjects(data.access_token);
      loadTasks(data.access_token);
    } catch (error) {
      console.error(error);
      setMessage("Unable to connect to server.");
    }
  };
const loadProjects = async (token) => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/projects",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      console.error("Failed to load projects");
      return;
    }

    const data = await response.json();
    setProjects(data);
  } catch (error) {
    console.error("Error loading projects:", error);
  }
};

const loadTasks = async (token) => {
  console.log("LOAD TASKS CALLED");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/tasks",
      {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    if (!response.ok) {
      console.error("Failed to load tasks");
      return;
    }

    const data = await response.json();

    console.log("TASKS FROM BACKEND:", data);

    setTasks(data);
  } catch (error) {
    console.error("Error loading tasks:", error);
  }
};
  const handleCreateProject = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch("http://127.0.0.1:8000/projects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: projectName,
          description: projectDescription,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to create project");
        return;
      }

      setProjects([...projects, data]);

      setProjectName("");
      setProjectDescription("");
      setShowProjectForm(false);

      alert("Project created successfully! 🎉");
    } catch (error) {
      console.error(error);
      alert("Unable to connect to server.");
    }
  };

  const handleCreateTask = async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/tasks",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
          title: taskTitle,
          priority: taskPriority,
          due_date: taskDueDate || null,
          project_id: Number(taskProjectId),
        }),
      }
    );
    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to create task");
      return;
    }

    setTasks([...tasks, data]);

    setTaskTitle("");
    setTaskPriority("medium");
    setTaskDueDate("");
    setTaskProjectId("");
    setShowTaskForm(false);

    alert("Task created successfully! 🎉");
  } catch (error) {
    console.error(error);
    alert("Unable to connect to server.");
  }
};
  
  const handleUpdateTaskStatus = async (taskId, currentStatus) => {
   const token = localStorage.getItem("access_token");

   const newStatus =
    currentStatus === "completed" ? "pending" : "completed";

   try {
    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${taskId}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
          status: newStatus,
        }),
      }
    );

      const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to update task");
      return;
    }

    setTasks(
      tasks.map((task) =>
        task.id === taskId ? data : task
      )
    );
  } catch (error) {
    console.error(error);
    alert("Unable to connect to server.");
  }
};

const handleDeleteTask = async (taskId) => {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${taskId}`,
      {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to delete task");
      return;
    }

    setTasks(
      tasks.filter((task) => task.id !== taskId)
    );

    alert("Task deleted successfully! 🗑️");
  } catch (error) {
    console.error(error);
    alert("Unable to connect to server.");
  }
};

  const handleDeleteProject = async (projectId) => {
  const token = localStorage.getItem("access_token");

  const confirmDelete = window.confirm(
    "Are you sure you want to delete this project? Its tasks will also be deleted."
  );

  if (!confirmDelete) return;

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/projects/${projectId}`,
      {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to delete project");
      return;
    }

    setProjects(
      projects.filter((project) => project.id !== projectId)
    );

    setTasks(
      tasks.filter((task) => task.project_id !== projectId)
    );

    alert("Project deleted successfully! 🗑️");
  } catch (error) {
    console.error(error);
    alert("Unable to connect to server.");
  }
};
   

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setLoggedIn(false);
    setProjects([]);
     setTasks([]);
  };

  const filteredTasks = tasks.filter((task) => {
  const matchesSearch = task.title
    .toLowerCase()
    .includes(searchTerm.toLowerCase());

  const matchesPriority =
    priorityFilter === "all" ||
    task.priority === priorityFilter;

  return matchesSearch && matchesPriority;
});

 if (loggedIn) {
  const pendingTasks = tasks.filter(
    (task) => task.status === "pending"
  ).length;

  const completedTasks = tasks.filter(
    (task) => task.status === "completed"
  ).length;

  return (
    <div style={styles.dashboard}>
      <style>{`
  @keyframes livePulse {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }

    50% {
      opacity: 0.3;
      transform: scale(0.75);
    }
  }
`}</style>

      {/* HEADER */}
      <nav style={styles.navbar}>
        <div>
          <h2 style={styles.logo}>TaskFlow</h2>
          <p style={styles.headerSubtitle}>
            Task Management Dashboard
          </p>
        </div>

        <div style={styles.liveStatus}>
  <span style={styles.liveDot}></span>
  Live
</div>

        <button
          style={styles.logoutButton}
          onClick={handleLogout}
        >
          Logout
        </button>
      </nav>

      <main style={styles.main}>

        {/* WELCOME */}
        <div style={styles.welcome}>
         <h1 style={styles.welcomeTitle}>
  Welcome to TaskFlow 👋
</h1>
<p style={styles.welcomeSubtitle}>
  Manage your projects and tasks efficiently.
</p>
        </div>

        {/* STAT CARDS */}
        <div style={styles.stats}>

          <div style={styles.statCard}>
            <div style={styles.statIcon}>📋</div>
            <div>
              <p style={styles.statLabel}>TOTAL TASKS</p>
              <h2>{tasks.length}</h2>
            </div>
          </div>

          <div style={styles.statCard}>
            <div style={styles.statIcon}>⏳</div>
            <div>
              <p style={styles.statLabel}>PENDING</p>
              <h2>{pendingTasks}</h2>
            </div>
          </div>

          <div style={styles.statCard}>
            <div style={styles.statIcon}>✅</div>
            <div>
              <p style={styles.statLabel}>COMPLETED</p>
              <h2>{completedTasks}</h2>
            </div>
          </div>

        </div>

        {/* ADD TASK */}
        <section style={styles.section}>

          <div style={styles.sectionHeader}>
            <div>
              <h2>Add New Task</h2>
              <p style={styles.sectionSubtitle}>
                Create and organize your work
              </p>
            </div>

            <button
              style={styles.primaryButton}
              onClick={() =>
                setShowTaskForm(!showTaskForm)
              }
            >
              {showTaskForm ? "Close" : "+ Add Task"}
            </button>
          </div>

          {showTaskForm && (
            <form
              onSubmit={handleCreateTask}
              style={styles.taskForm}
            >

              <div style={styles.formGroup}>
                <label>Task Title</label>

                <input
                  type="text"
                  placeholder="Enter task title"
                  value={taskTitle}
                  onChange={(e) =>
                    setTaskTitle(e.target.value)
                  }
                  style={styles.input}
                  required
                />
              </div>

              <div style={styles.formRow}>

                <div style={styles.formGroup}>
                  <label>Priority</label>

                  <select
                    value={taskPriority}
                    onChange={(e) =>
                      setTaskPriority(e.target.value)
                    }
                    style={styles.input}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <div style={styles.formGroup}>
                  <label>Due Date</label>

                  <input
                    type="date"
                    value={taskDueDate}
                    onChange={(e) =>
                      setTaskDueDate(e.target.value)
                    }
                    style={styles.input}
                  />
                </div>

                <div style={styles.formGroup}>
                  <label>Project</label>

                  <select
                    value={taskProjectId}
                    onChange={(e) =>
                      setTaskProjectId(e.target.value)
                    }
                    style={styles.input}
                    required
                  >
                    <option value="">
                      Select Project
                    </option>

                    {projects.map((project) => (
                      <option
                        key={project.id}
                        value={project.id}
                      >
                        {project.name}
                      </option>
                    ))}
                  </select>
                </div>

              </div>

              <button
                type="submit"
                style={styles.createButton}
              >
                Create Task
              </button>

            </form>
          )}

        </section>

        {/* TASK LIST */}
        <section style={styles.section}>

          <div style={styles.sectionHeader}>
            <div>
              <h2 style={styles.sectionTitle}>My Tasks</h2>
            
             <p style={styles.sectionDescription}>
  Track your current work
</p>
            </div>
          </div>

          <div style={styles.taskToolbar}>

            <input
  type="text"
  placeholder="🔍 Search tasks..."
  value={searchTerm}
  onChange={(e) => setSearchTerm(e.target.value)}
  style={styles.searchInput}
/>

           <select
  value={priorityFilter}
  onChange={(e) => setPriorityFilter(e.target.value)}
  style={styles.filterInput}
>
  <option value="all">All Priorities</option>
  <option value="high">High</option>
  <option value="medium">Medium</option>
  <option value="low">Low</option>
</select>

          </div>

          {tasks.length === 0 ? (
            <div style={styles.emptyState}>
              <h3>No tasks yet</h3>
              <p>
                Create your first task to get started.
              </p>
            </div>
          ) : (
            <div style={styles.taskGrid}>

              {filteredTasks.map((task) => (

                <div
                  key={task.id}
                  style={styles.taskCard}
                >

                  <div style={styles.taskHeader}>
                    <h3>{task.title}</h3>

                    <span
                      style={{
                        ...styles.statusBadge,
                        background:
                          task.status === "completed"
                            ? "#14532d"
                            : "#713f12",
                        color:
                          task.status === "completed"
                            ? "#86efac"
                            : "#fde047",
                      }}
                    >
                      {task.status}
                    </span>
                  </div>

                  <div style={styles.taskDetails}>

                    <p>
                      Priority:
                      <strong> {task.priority}</strong>
                    </p>

                    <p>
                      Due date:
                      <strong>
                        {" "}
                        {task.due_date || "Not set"}
                      </strong>
                    </p>

                  </div>

                  <div style={styles.taskActions}>

                    <button
                      style={styles.statusButton}
                      onClick={() =>
                        handleUpdateTaskStatus(
                          task.id,
                          task.status
                        )
                      }
                    >
                      {task.status === "completed"
                        ? "Mark Pending"
                        : "Mark Complete"}
                    </button>
                    <button
  style={styles.deleteButton}
  onClick={() => handleDeleteTask(task.id)}
>
  🗑 Delete
</button>

                  </div>

                </div>

              ))}

            </div>
          )}

        </section>

        {/* PROJECTS */}
        <section style={styles.section}>

          <div style={styles.sectionHeader}>

            <div>
              <h2>My Projects</h2>
              <p style={styles.sectionSubtitle}>
                Organize your tasks by project
              </p>
            </div>

            <button
              style={styles.primaryButton}
              onClick={() =>
                setShowProjectForm(!showProjectForm)
              }
            >
              {showProjectForm
                ? "Close"
                : "+ Create Project"}
            </button>

          </div>

          {showProjectForm && (
            <form
              onSubmit={handleCreateProject}
              style={styles.taskForm}
            >

              <div style={styles.formGroup}>
                <label>Project Name</label>

                <input
                  type="text"
                  placeholder="Enter project name"
                  value={projectName}
                  onChange={(e) =>
                    setProjectName(e.target.value)
                  }
                  style={styles.input}
                  required
                />
              </div>

              <div style={styles.formGroup}>
                <label>Description</label>

                <textarea
                  placeholder="Enter project description"
                  value={projectDescription}
                  onChange={(e) =>
                    setProjectDescription(e.target.value)
                  }
                  style={styles.textarea}
                  rows="3"
                />
              </div>

              <button
                type="submit"
                style={styles.createButton}
              >
                Create Project
              </button>

            </form>
          )}

          {projects.length === 0 ? (
            <div style={styles.emptyState}>
              <h3>No projects yet</h3>
              <p>
                Create your first project to get started.
              </p>
            </div>
          ) : (
            <div style={styles.projectGrid}>

              {projects.map((project) => (

                <div
                  key={project.id}
                  style={styles.projectCard}
                >

                  <h3>{project.name}</h3>

                  <p>
                    {project.description ||
                      "No description"}
                  </p>
                   <button
  style={styles.deleteButton}
  onClick={() => handleDeleteProject(project.id)}
>
  🗑 Delete
</button>
                </div>

              ))}

            </div>
          )}

        </section>

      </main>
    </div>
  );
}       
  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1>TaskFlow</h1>

        <p style={styles.subtitle}>
          Manage your projects and tasks
        </p>

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
            required
          />

          <button type="submit" style={styles.button}>
            Login
          </button>
        </form>

        {message && (
          <p style={styles.message}>{message}</p>
        )}
      </div>
    </div>
  );
}

const styles = {

  text: {
  color: "#f8fafc",
  },

mutedText: {
  color: "#cbd5e1",
  },

  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a",
    fontFamily: "Arial, sans-serif",
  },

  card: {
    width: "380px",
    padding: "40px",
    background:  "#1e293b",
    borderRadius: "16px",
    boxShadow: "0 10px 40px rgba(0,0,0,0.4)",
  },

  subtitle: {
    color: "#94a3b8",
    marginBottom: "25px",
  },

  input: {
  width: "100%",
  padding: "13px",
  marginBottom: "15px",
  border: "1px solid #475569",
  borderRadius: "8px",
  boxSizing: "border-box",
  fontSize: "15px",
  background: "#0f172a",
  color: "#f8fafc",
  },

 textarea: {
  width: "100%",
  padding: "13px",
  border: "1px solid #344b73",
  borderRadius: "8px",
  boxSizing: "border-box",
  fontSize: "15px",
  background: "#0b1730",
  color: "#ffffff",
  resize: "vertical",
},

  button: {
    width: "100%",
    padding: "12px",
    border: "none",
    borderRadius: "6px",
    background: "#2563eb",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
  },

  message: {
    marginTop: "20px",
    textAlign: "center",
  },

 dashboard: {
  minHeight: "100vh",
  background: "#08111f",
  color: "#f8fafc",
  fontFamily: "Arial, sans-serif",
},

navbar: {
  minHeight: "82px",
  background: "#10234d",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  padding: "0 45px",
  borderBottom: "1px solid #263b70",
  boxSizing: "border-box",
},
 
logo: {
  color: "#ffffff",
  margin: 0,
  fontSize: "25px",
  fontWeight: "800",
  letterSpacing: "1px",
},

logoutButton: {
  padding: "10px 20px",
  border: "1px solid #475569",
  borderRadius: "8px",
  background: "#0f172a",
  color: "#f8fafc",
  cursor: "pointer",
},

headerSubtitle: {
  margin: "6px 0 0",
  color: "#94a3b8",
  fontSize: "12px",
  letterSpacing: "2px",
},

main: {
   padding: "40px 35px 70px",
  maxWidth: "1150px",
  margin: "auto",
  boxSizing: "border-box",
  },

welcome: {
  marginBottom: "32px",
  color: "#f8fafc",
},

welcomeTitle: {
  margin: 0,
  color: "#f8fafc",
  fontSize: "32px",
  fontWeight: "800",
  lineHeight: "1.2",
  letterSpacing: "-0.5px",
},

welcomeSubtitle: {
  margin: "10px 0 0",
  color: "#94a3b8",
  fontSize: "15px",
  lineHeight: "1.6",
},

  stats: {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "18px",
  marginTop: "30px",
 },

 statIcon: {
  width: "52px",
  height: "52px",
  borderRadius: "12px",
  background: "#172f63",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: "23px",
},

statLabel: {
  margin: 0,
  color: "#8fa3c7",
  fontSize: "12px",
  fontWeight: "700",
  letterSpacing: "1px",
},

 statCard: {
  background: "#111f38",
  padding: "22px",
  borderRadius: "14px",
  border: "1px solid #263b5e",
  display: "flex",
  alignItems: "center",
  gap: "16px",
  boxShadow: "0 8px 25px rgba(0,0,0,0.22)",
  boxSizing: "border-box",
},


  section: {
  marginTop: "25px",
  background: "#111f38",
  padding: "28px",
  borderRadius: "15px",
  boxShadow: "0 8px 25px rgba(0,0,0,0.2)",
  border: "1px solid #263b5e",
  color: "#f8fafc",
  },

  sectionTitle: {
  margin: 0,
  color: "#f8fafc",
  fontSize: "22px",
  fontWeight: "700",
},

sectionDescription: {
  margin: "6px 0 0",
  color: "#94a3b8",
  fontSize: "14px",
},

  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "24px",
  },

  sectionSubtitle: {
  margin: "5px 0 0",
  color: "#8fa3c7",
  fontSize: "13px",
},

  primaryButton: {
  padding: "11px 18px",
  border: "none",
  borderRadius: "8px",
  background: "#2563eb",
  color: "white",
  cursor: "pointer",
  fontSize: "14px",
  fontWeight: "600",
  },

  deleteButton: {
  marginTop: "10px",
  padding: "10px 18px",
  border: "none",
  borderRadius: "7px",
  background: "#dc2626",
  color: "white",
  cursor: "pointer",
  fontSize: "14px",
  fontWeight: "600",
  },

 
  emptyState: {
    textAlign: "center",
    padding: "40px",
    color: "#777",
  },

 projectGrid: {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "18px",
  },

  projectsCard: {
  background: "#172033",
  padding: "30px",
  borderRadius: "16px",
  border: "1px solid #334155",
},

cardTitle: {
  marginTop: 0,
  color: "#f8fafc",
},

label: {
  display: "block",
  marginTop: "20px",
  marginBottom: "8px",
  color: "#cbd5e1",
  fontSize: "13px",
  fontWeight: "700",
  letterSpacing: "1px",
},

darkInput: {
  width: "100%",
  padding: "14px",
  boxSizing: "border-box",
  background: "#0f172a",
  color: "#f8fafc",
  border: "1px solid #334155",
  borderRadius: "9px",
  fontSize: "15px",
  outline: "none",
  marginBottom: "8px",
},

addTaskButton: {
  width: "100%",
  marginTop: "22px",
  padding: "14px",
  border: "none",
  borderRadius: "9px",
  background: "#2563eb",
  color: "#fff",
  fontSize: "16px",
  fontWeight: "700",
  cursor: "pointer",
},


  filterBar: {
  display: "flex",
  gap: "15px",
  marginBottom: "25px",
  flexWrap: "wrap",
  },

  formGroup: {
  display: "flex",
  flexDirection: "column",
  gap: "8px",
  marginBottom: "18px",
},

formRow: {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "18px",
},

  taskForm: {
  background: "#0b1730",
  border: "1px solid #263b5e",
  padding: "24px",
  borderRadius: "12px",
  marginBottom: "25px",
},

  taskFormCard: {
  background: "#172033",
  padding: "30px",
  borderRadius: "16px",
  border: "1px solid #334155",
  marginBottom: "30px",
},

taskListCard: {
  background: "#172033",
  padding: "30px",
  borderRadius: "16px",
  border: "1px solid #334155",
  marginBottom: "30px",
},

  statusBadge: {
  display: "inline-block",
  padding: "5px 10px",
  borderRadius: "20px",
  fontSize: "11px",
  fontWeight: "700",
  textTransform: "uppercase",
  },

  taskActions: {
  display: "flex",
  gap: "10px",
  marginTop: "15px",
  flexWrap: "wrap",
  },
  description: {
  color: "#cbd5e1",
  },

  listHeader: {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: "20px",
},

taskTop: {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "15px",
},

taskInfo: {
  color: "#cbd5e1",
  fontSize: "14px",
},

taskDetails: {
  marginTop: "15px",
  color: "#aebed8",
  fontSize: "14px",
  lineHeight: "1.7",
},

statusButton: {
  marginTop: "10px",
  padding: "9px 14px",
  border: "1px solid #475569",
  borderRadius: "7px",
  background: "#172554",
  color: "#f8fafc",
  cursor: "pointer",
},

secondaryButton: {
  padding: "10px 16px",
  border: "1px solid #475569",
  borderRadius: "8px",
  background: "#172554",
  color: "#f8fafc",
  cursor: "pointer",
},

projectForm: {
  padding: "20px",
  background: "#0f172a",
  borderRadius: "10px",
  marginBottom: "20px",
},


projectCard: {
  padding: "20px",
  border: "1px solid #2b4267",
  borderRadius: "11px",
  background: "#0b1730",
  color: "#f8fafc",
},

createButton: {
  padding: "12px 22px",
  border: "none",
  borderRadius: "8px",
  background: "#2563eb",
  color: "#ffffff",
  cursor: "pointer",
  fontWeight: "700",
},

taskToolbar: {
  display: "grid",
  gridTemplateColumns: "1fr 190px",
  gap: "12px",
  marginBottom: "22px",
},

searchInput: {
  width: "100%",
  padding: "13px 15px",
  boxSizing: "border-box",
  borderRadius: "8px",
  border: "1px solid #344b73",
  background: "#0b1730",
  color: "#ffffff",
  fontSize: "14px",
},

filterInput: {
  width: "100%",
  padding: "13px 15px",
  boxSizing: "border-box",
  borderRadius: "8px",
  border: "1px solid #344b73",
  background: "#0b1730",
  color: "#ffffff",
  fontSize: "14px",
},

taskGrid: {
  display: "grid",
  gridTemplateColumns: "repeat(2, 1fr)",
  gap: "18px",
},

taskCard: {
  background: "#0b1730",
  padding: "21px",
  borderRadius: "12px",
  border: "1px solid #263b5e",
},

taskHeader: {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "15px",
},

liveStatus: {
  display: "flex",
  alignItems: "center",
  gap: "7px",
  color: "#22c55e",
  fontSize: "13px",
  fontWeight: "600",
},

liveDot: {
  width: "8px",
  height: "8px",
  borderRadius: "50%",
  background: "#22c55e",
  boxShadow: "0 0 8px #22c55e",
  animation: "livePulse 2.2s ease-in-out infinite",
},


};


export default App;


