#!/usr/bin/env python3

import boto3
from datetime import datetime, timedelta

def get_ec2_metrics(instance_id):
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    datapoints = metrics['Datapoints']
    if datapoints:
        avg_cpu = sorted(datapoints, key=lambda x: x['Timestamp'])[-1]['Average']
        return f"{avg_cpu:.2f}%"
    else:
        return "No data"

def list_instances_and_metrics():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    report_lines = []
    print("\nMonitoreo de Instancias EC2:\n" + "-" * 50)
    for instance in instances:
        cpu_util = get_ec2_metrics(instance.id)
        print(f"ID: {instance.id} | CPU Utilization (Última Hora): {cpu_util}")
        report_lines.append(f"ID: {instance.id} | CPU Utilization (Última Hora): {cpu_util}")

    return report_lines

def save_report(report_data):
    filename = f"cloudwatch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write("\n".join(report_data))
    print(f"\nReporte guardado en: {filename}")

if __name__ == "__main__":
    data = list_instances_and_metrics()
    if data:
        save_report(data)
    else:
        print("No hay instancias en ejecución.")

