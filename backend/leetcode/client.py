import requests
from datetime import datetime, timezone

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

def get_user_profile(username):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        solvedProblem: submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    try:
        response = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": {"username": username}},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        data = response.json()
        if not data.get("data", {}).get("matchedUser"):
            return None
        return data["data"]["matchedUser"]
    except Exception:
        return None

def get_solved_problems(username):
    query = """
    query getSolvedProblems($username: String!) {
      recentSubmissionList(username: $username, limit: 100) {
        titleSlug
        statusDisplay
        timestamp
      }
    }
    """
    try:
        response = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": {"username": username}},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        data = response.json()
        return data.get("data", {}).get("recentSubmissionList", [])
    except Exception:
        return []

def validate_username(username):
    result = get_user_profile(username)
    return result is not None

def get_total_solved(username):
    profile = get_user_profile(username)
    if not profile:
        return 0
    stats = profile.get("submitStats", {}).get("acSubmissionNum", [])
    for s in stats:
        if s["difficulty"] == "All":
            return s["count"]
    return 0


def check_problem_solved(lc_username, problem_slug, after_date):
    """
    Verify via LeetCode GraphQL that a user has an Accepted submission
    for the given problem after a specific date.
    Returns: (solved: bool, solved_at: datetime|None)
    """
    query = """
    query getSolvedProblems($username: String!) {
      recentSubmissionList(username: $username, limit: 20) {
        titleSlug
        statusDisplay
        timestamp
      }
    }
    """
    try:
        response = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": {"username": lc_username}},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        submissions = response.json().get("data", {}).get("recentSubmissionList", []) or []
        for sub in submissions:
            if sub.get("titleSlug") == problem_slug and sub.get("statusDisplay") == "Accepted":
                ts = datetime.fromtimestamp(int(sub["timestamp"]), tz=timezone.utc)
                if ts.date() >= after_date:
                    return True, ts
        return False, None
    except Exception:
        return False, None
