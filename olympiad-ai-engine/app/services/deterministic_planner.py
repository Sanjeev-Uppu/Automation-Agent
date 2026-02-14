def generate_fallback_plan(duration_days, chapter_name):

    plan = []

    for i in range(1, duration_days + 1):

        if i % 7 == 0:
            task = "Full Revision + Practice Questions"
        elif i % 5 == 0:
            task = "Mock Test Practice"
        else:
            task = "Concept Study + Notes"

        plan.append({
            "day": i,
            "topics": f"{chapter_name} - Section {i}",
            "tasks": task
        })

    return {
        "duration_days": duration_days,
        "chapter": chapter_name,
        "plan": plan
    }
