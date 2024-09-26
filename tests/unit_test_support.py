from codeflare_sdk.cluster.cluster import (
    Cluster,
    ClusterConfiguration,
)


def createClusterConfig():
    config = ClusterConfiguration(
        name="unit-test-cluster",
        namespace="ns",
        num_workers=2,
        worker_cpu_requests=3,
        worker_cpu_limits=4,
        worker_memory_requests=5,
        worker_memory_limits=6,
        worker_extended_resource_requests={"nvidia.com/gpu": 7},
        appwrapper=True,
        machine_types=["cpu.small", "gpu.large"],
        image_pull_secrets=["unit-test-pull-secret"],
        write_to_file=True,
    )
    return config


def createClusterWithConfig(mocker):
    mocker.patch("kubernetes.config.load_kube_config", return_value="ignore")
    mocker.patch(
        "kubernetes.client.CustomObjectsApi.get_cluster_custom_object",
        return_value={"spec": {"domain": "apps.cluster.awsroute.org"}},
    )
    cluster = Cluster(createClusterConfig())
    return cluster


def createClusterWrongType():
    config = ClusterConfiguration(
        name="unit-test-cluster",
        namespace="ns",
        num_workers=2,
        worker_cpu_requests=[],
        worker_cpu_limits=4,
        worker_memory_requests=5,
        worker_memory_limits=6,
        worker_extended_resource_requests={"nvidia.com/gpu": 7},
        appwrapper=True,
        machine_types=[True, False],
        image_pull_secrets=["unit-test-pull-secret"],
        image="quay.io/modh/ray:2.35.0-py39-cu121-b87d9a71c34c0b79c0e7aa9d4245fe7f0065f774",
        write_to_file=True,
        labels={1: 1},
    )
    return config


def get_package_and_version(package_name, requirements_file_path):
    with open(requirements_file_path, "r") as file:
        for line in file:
            if line.strip().startswith(f"{package_name}=="):
                return line.strip()
    return None
