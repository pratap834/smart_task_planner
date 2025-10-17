"""
AWS S3 Service for file storage and exports
"""
import boto3
from botocore.exceptions import ClientError
from config import settings
import json
import logging
from typing import Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class S3Service:
    """Service for AWS S3 operations"""
    
    def __init__(self):
        """Initialize S3 client"""
        self.enabled = bool(settings.AWS_S3_BUCKET and settings.AWS_ACCESS_KEY_ID)
        
        if self.enabled:
            self.s3_client = boto3.client(
                's3',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.bucket_name = settings.AWS_S3_BUCKET
            logger.info(f"✓ S3 service initialized for bucket: {self.bucket_name}")
        else:
            logger.warning("⚠ S3 service not configured - file exports disabled")
    
    async def export_plan_to_s3(self, plan_id: str, plan_data: dict) -> Optional[str]:
        """
        Export a plan to S3 as JSON
        
        Args:
            plan_id: Plan identifier
            plan_data: Plan data dictionary
            
        Returns:
            S3 file URL or None if S3 not configured
        """
        if not self.enabled:
            return None
        
        try:
            # Generate file key
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            file_key = f"plans/plan_{plan_id}_{timestamp}.json"
            
            # Convert plan data to JSON
            json_content = json.dumps(plan_data, indent=2, default=str)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=json_content.encode('utf-8'),
                ContentType='application/json',
                Metadata={
                    'plan_id': str(plan_id),
                    'exported_at': timestamp
                }
            )
            
            # Generate S3 URL
            file_url = f"s3://{self.bucket_name}/{file_key}"
            logger.info(f"✓ Plan {plan_id} exported to S3: {file_url}")
            
            return file_url
            
        except ClientError as e:
            logger.error(f"✗ Failed to export plan to S3: {e}")
            return None
    
    async def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for downloading a file
        
        Args:
            file_key: S3 object key
            expiration: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Presigned URL or None if failed
        """
        if not self.enabled:
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key
                },
                ExpiresIn=expiration
            )
            
            logger.info(f"✓ Generated presigned URL for {file_key}")
            return url
            
        except ClientError as e:
            logger.error(f"✗ Failed to generate presigned URL: {e}")
            return None
    
    async def upload_file(self, file_content: bytes, file_key: str, content_type: str = 'application/octet-stream') -> Optional[str]:
        """
        Upload a file to S3
        
        Args:
            file_content: File content as bytes
            file_key: S3 object key (file path)
            content_type: MIME type of the file
            
        Returns:
            S3 file URL or None if failed
        """
        if not self.enabled:
            return None
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=content_type
            )
            
            file_url = f"s3://{self.bucket_name}/{file_key}"
            logger.info(f"✓ File uploaded to S3: {file_url}")
            
            return file_url
            
        except ClientError as e:
            logger.error(f"✗ Failed to upload file to S3: {e}")
            return None
    
    async def delete_file(self, file_key: str) -> bool:
        """
        Delete a file from S3
        
        Args:
            file_key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            logger.info(f"✓ File deleted from S3: {file_key}")
            return True
            
        except ClientError as e:
            logger.error(f"✗ Failed to delete file from S3: {e}")
            return False
    
    async def list_plan_exports(self, plan_id: str) -> list:
        """
        List all exports for a specific plan
        
        Args:
            plan_id: Plan identifier
            
        Returns:
            List of export file keys
        """
        if not self.enabled:
            return []
        
        try:
            prefix = f"plans/plan_{plan_id}_"
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            return []
            
        except ClientError as e:
            logger.error(f"✗ Failed to list plan exports: {e}")
            return []


# Create singleton instance
s3_service = S3Service()
