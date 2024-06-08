import requests
import unittest


class TestHelloWorldDAG(unittest.TestCase):

    def test_dag_status(self):
        auth = ("airflow", "airflow")
        response = requests.get(
            "http://localhost:8080/api/v1/dags/Hello-world", auth=auth
        )
        self.assertEqual(response.status_code, 200)
        dag_info = response.json()
        self.assertEqual(dag_info["dag_id"], "Hello-world")

    def test_task_status(self):
        auth = ("airflow", "airflow")
        response = requests.get(
            "http://localhost:8080/api/v1/dags/Hello-world/dagRuns", auth=auth
        )
        self.assertEqual(response.status_code, 200)
        dag_runs = response.json()["dag_runs"]

        if not dag_runs:
            print("No DAG runs found. Skipping task status test.")
            return

        dag_run_id = dag_runs[0]["dag_run_id"]

        response = requests.get(
            f"http://localhost:8080/api/v1/dags/Hello-world/dagRuns/{dag_run_id}/taskInstances",
            auth=auth,
        )
        self.assertEqual(response.status_code, 200)
        task_instances = response.json()["task_instances"]

        self.assertTrue(len(task_instances) > 0, "No task instances found")
        for task_instance in task_instances:
            self.assertEqual(task_instance["state"], "success")


if __name__ == "__main__":
    unittest.main()