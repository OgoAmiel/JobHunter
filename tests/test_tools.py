from app.tools import find_demo_jobs


def test_search_accounting_jobs():
    jobs = find_demo_jobs("graduate accounting jobs")

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Graduate Finance Assistant"


def test_search_software_jobs():
    jobs = find_demo_jobs("graduate software jobs")

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Graduate Software Developer"


def test_search_no_matching_jobs():
    jobs = find_demo_jobs("graduate agriculture jobs")

    assert len(jobs) == 0


def test_search_empty_keyword():
    jobs = find_demo_jobs("")

    assert jobs == []
