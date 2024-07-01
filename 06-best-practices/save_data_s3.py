import pandas as pd
import boto3
from io import BytesIO

def save_data(df, bucket, key):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())

# Example usage
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
save_data(df, 'your-s3-bucket', 'your-file-key.csv')