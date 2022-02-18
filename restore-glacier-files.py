import boto3
import argparse

parser = argparse.ArgumentParser(description='restore object(s) from AWS Glacier')
parser.add_argument('mode', help='mode of restoration (Single|RecursiveFolder|RecursiveBucket)')
parser.add_argument('type', help='type of restore retrieval (Standard|Bulk|Expedited)')
parser.add_argument('days', type=int, help='number of days object(s) will be restored')
parser.add_argument('--version', '-v', action='version',version='%(prog)s 1.0')

args = parser.parse_args()
client = boto3.client('s3')

if args.mode == 'Single':
    bucket = input("Name of s3 bucket: ")
    key = input("Key of s3 object: ")
    client.restore_object(
        Bucket = bucket,
        Key = key,
        RestoreRequest = {
            'Days' : args.days,
            'GlacierJobParameters':{
                'Tier' : args.type
            }
        }
    )

elif args.mode == 'RecursiveFolder' or args.mode == 'RecursiveBucket':
    if args.mode == 'RecursiveFolder':
        uri = input("S3 URI of root folder (example: s3://pics/2021/): ")
    elif args.mode == 'RecursiveBucket':
        uri = input("S3 URI of bucket (example: s3://pics/): ")
    root_folder_prefix = uri.split('/',3)  
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(root_folder_prefix[2])
    with open('restored_files.txt', 'w') as f:
        for object in bucket.objects.filter(Prefix=root_folder_prefix[3]):
            if object.size > 0:
                try:
                    client.restore_object(
                        Bucket = root_folder_prefix[2],
                        Key = object.key,
                        RestoreRequest = {
                            'Days' : args.days,
                            'GlacierJobParameters':{
                                'Tier' : args.type
                            }
                        }
                    )
                except:
                    print(f"File {object.key} is not archived in Glacier. Continuing with rest of objects..")
                f.write(f"{object.key} {round(object.size * 0.000001, 6)}\n")
                