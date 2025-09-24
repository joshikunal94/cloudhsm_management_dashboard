from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
import subprocess
import os
import json
from app.services.cloudhsm_service import CloudHSMService

router = APIRouter(prefix="/hsm", tags=["hsm-config"])

@router.get("/health")
async def check_hsm_connection():
    """Check HSM connection status (unauthenticated)"""
    try:
        # Check if certificate exists
        cert_exists = Path("/opt/cloudhsm/etc/customerCA.crt").exists()
        
        # Check if IP address is configured in PCKS11 config
        pkcs11_configured = False
        pkcs11_config_file = Path("/opt/cloudhsm/etc/cloudhsm-pkcs11.cfg")
        if pkcs11_config_file.exists():
            with open(pkcs11_config_file, "r") as f:
                config_json = json.loads(f.read())
                cluster = config_json.get("clusters", [{}])[0]
                for server in cluster.get('cluster', {}).get('servers', []):
                    ip_address = server.get('hostname')
                    host_enabled = server.get('enable', False)
                    if ip_address and host_enabled:
                        pkcs11_configured = True
                        break
        
        # check connection with PyKCS11
        hsm_service = CloudHSMService()
        session_connected = hsm_service.check_connection()
        
        
        return {
            "connected": session_connected,
            "configured": pkcs11_configured,
            "certificate_exists": cert_exists
        }
    except Exception as e:
        return {
            "connected": False,
            "configured": False,
            "certificate_exists": False,
            "error": str(e)
        }

@router.post("/configure")
async def configure_hsm(
    ip_address: str = Form(...),
    certificate: UploadFile = File(...)
):
    """Configure HSM connection (unauthenticated)"""
    try:
        # Validate IP address format
        if not ip_address or len(ip_address.split('.')) != 4:
            raise HTTPException(status_code=400, detail="Invalid IP address format")
        
        # Read certificate content
        cert_content = await certificate.read()
        if not cert_content:
            raise HTTPException(status_code=400, detail="Certificate file is empty")
        
        # Write certificate to temp location first
        temp_cert_path = "/tmp/customerCA.crt"
        with open(temp_cert_path, "wb") as f:
            f.write(cert_content)
        
        # Copy certificate to required location using sudo
        copy_result = subprocess.run([
            "sudo", "cp", temp_cert_path, "/opt/cloudhsm/etc/customerCA.crt"
        ], capture_output=True, text=True)
        
        if copy_result.returncode != 0:
            return {
                "success": False,
                "message": f"Failed to copy certificate: {copy_result.stderr}"
            }
        
        # Set proper permissions using sudo
        chmod_result = subprocess.run([
            "sudo", "chmod", "644", "/opt/cloudhsm/etc/customerCA.crt"
        ], capture_output=True, text=True)
        
        if chmod_result.returncode != 0:
            return {
                "success": False,
                "message": f"Failed to set permissions: {chmod_result.stderr}"
            }
        
        # Clean up temp file
        os.remove(temp_cert_path)
        
        # Configure PKCS11 with IP address
        config_result = subprocess.run([
            "sudo", "/opt/cloudhsm/bin/configure-pkcs11", "-a", ip_address
        ], capture_output=True, text=True)
        
        if config_result.returncode != 0:
            return {
                "success": False,
                "message": f"PKCS11 configuration failed: {config_result.stderr}"
            }
        
        # Test the connection
        test_result = CloudHSMService().check_connection()
        if test_result:
            return {
                "success": True,
                "message": "HSM configured and connected successfully"
            }
        else:
            return {
                "success": False,
                "message": f"HSM configuration completed but connection test failed"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Connection test timed out. Check IP address and network connectivity."
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Configuration failed: {str(e)}"
        }

@router.post("/test-connection")
async def test_hsm_connection():
    """Test current HSM connection (unauthenticated)"""
    try:
        pkcs11_connected = CloudHSMService().check_connection()
        
        if pkcs11_connected :
            return {
                "success": True,
                "message": "HSM connection successful"
            }
        else:
            return {
                "success": False,
                "message": f"HSM connection failed"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "Connection test timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Connection test failed: {str(e)}"
        }