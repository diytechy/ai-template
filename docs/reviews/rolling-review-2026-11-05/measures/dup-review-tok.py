import sys
sys.path.insert(0, "/home/user/ai-template/project-trajectory/scripts")
import check, agent_session
t = "ruff check src #note --fix"
print("check._split_template :", check._split_template(t))
print("agent_session.split_cmd:", agent_session.split_cmd(t))
