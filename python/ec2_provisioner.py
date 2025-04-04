#!/usr/bin/env python3

import boto3
import sys
import time
from datetime import datetime

def create_ec2_instance(instance_type='t2.micro', ami_id='ami-00a929b66ed6e0de6', count=1):
    """
    Crea instancias EC2 con los parámetros especificados
    """
    ec2 = boto3.resource('ec2')
    
    # Verificar límites antes de crear
    current_instances = list(ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running', 'stopping', 'stopped']}]
    ))
    
    if len(current_instances) + count > 9:
        print(f"ERROR: No se pueden crear {count} instancias. Límite máximo de 9 instancias.")
        print(f"Instancias actuales: {len(current_instances)}")
        return None
    
    try:
        instances = ec2.create_instances(
            ImageId=ami_id,
            MinCount=count,
            MaxCount=count,
            InstanceType=instance_type,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'DevOps-Instance-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
                        },
                        {
                            'Key': 'Project',
                            'Value': 'SolucionesTecnologicas'
                        }
                    ]
                }
            ]
        )
        
        print(f"Creadas {count} instancias EC2 de tipo {instance_type}")
        return instances
    except Exception as e:
        print(f"Error al crear instancias: {str(e)}")
        return None

def list_ec2_instances():
    """
    Lista todas las instancias EC2 y su estado
    """
    ec2 = boto3.resource('ec2')
    instances = list(ec2.instances.all())
    
    print(f"\nTotal de instancias EC2: {len(instances)}")
    print("-" * 80)
    print(f"{'ID':20} {'Tipo':12} {'Estado':10} {'IP Pública':15} {'Nombre':25}")
    print("-" * 80)
    
    for instance in instances:
        name = 'N/A'
        for tag in instance.tags if instance.tags else []:
            if tag['Key'] == 'Name':
                name = tag['Value']
        
        print(f"{instance.id:20} {instance.instance_type:12} {instance.state['Name']:10} {instance.public_ip_address if instance.public_ip_address else 'N/A':15} {name:25}")

def list_s3_buckets():
    """
    Lista todos los buckets S3 y sus objetos
    """
    s3 = boto3.resource('s3')
    
    print("\nBuckets S3:")
    print("-" * 80)
    
    for bucket in s3.buckets.all():
        print(f"Bucket: {bucket.name}")
        print("Objetos:")
        
        try:
            count = 0
            for obj in bucket.objects.all():
                print(f"  - {obj.key} ({obj.size} bytes)")
                count += 1
                if count >= 10:
                    print("  ... (mostrando solo los primeros 10 objetos)")
                    break
            if count == 0:
                print("  [Bucket vacío]")
        except Exception as e:
            print(f"  Error al listar objetos: {str(e)}")
        
        print("-" * 80)

def generate_resource_report():
    """
    Genera un reporte de uso de recursos AWS
    """
    ec2 = boto3.resource('ec2')
    s3 = boto3.resource('s3')
    cloudwatch = boto3.client('cloudwatch')
    
    # Contar instancias por tipo
    instances = list(ec2.instances.all())
    instance_types = {}
    for instance in instances:
        if instance.instance_type in instance_types:
            instance_types[instance.instance_type] += 1
        else:
            instance_types[instance.instance_type] = 1
    
    # Contar buckets y estimar almacenamiento
    buckets = list(s3.buckets.all())
    
    # Crear reporte
    report = f"""
==========================================================
          REPORTE DE RECURSOS AWS
          {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
==========================================================

INSTANCIAS EC2:
--------------
Total: {len(instances)}

Distribución por tipo:
{chr(10).join([f"- {t}: {c}" for t, c in instance_types.items()])}

ALMACENAMIENTO S3:
-----------------
Total de buckets: {len(buckets)}

==========================================================
    """
    
    print(report)
    
    # Guardar reporte en archivo
    with open(f"aws_resources_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
        f.write(report)
    
    print(f"Reporte guardado en archivo aws_resources_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def main():
    if len(sys.argv) < 2:
        print("Uso: python ec2_provisioner.py [create|list|report|s3]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        instance_type = sys.argv[3] if len(sys.argv) > 3 else 't2.micro'
        create_ec2_instance(instance_type=instance_type, count=count)
    elif command == 'list':
        list_ec2_instances()
    elif command == 'report':
        generate_resource_report()
    elif command == 's3':
        list_s3_buckets()
    else:
        print("Comando no válido. Opciones: create, list, report, s3")

if __name__ == "__main__":
    main()
