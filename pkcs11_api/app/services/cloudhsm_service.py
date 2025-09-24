import PyKCS11
import os
from typing import Optional, List
from app.models.keys import KeyInfo, KeyDetailResponse
from app.models.key_schemas import CreateKeyRequest, DeleteKeyRequest, CreateKeyResponse, DeleteKeyResponse

class CloudHSMService:
    def __init__(self):
        self.pkcs11_lib = os.getenv("PKCS11_LIB", "/opt/cloudhsm/lib/libcloudhsm_pkcs11.so")
        self.session = None
        self.pkcs11 = None
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with CloudHSM using PyKCS11"""
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                print("No slots found")
                return False
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login with combined username:password as PIN
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # If we reach here, authentication was successful
            return True
            
        except PyKCS11.PyKCS11Error as e:
            print(f"CloudHSM authentication failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error during authentication: {e}")
            return False
    
    def list_keys(self, username: str, password: str) -> List[KeyInfo]:
        """List all keys in CloudHSM"""
        keys = []
        
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return keys
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # Find all objects
            objects = self.session.findObjects()
            
            for obj in objects:
                try:
                    # Get object attributes
                    attrs = self.session.getAttributeValue(obj, [
                        PyKCS11.CKA_CLASS,
                        PyKCS11.CKA_KEY_TYPE,
                        PyKCS11.CKA_LABEL,
                        PyKCS11.CKA_ID
                    ])
                    
                    key_info = self._create_key_info(attrs)
                    if key_info:
                        keys.append(key_info)
                    
                except Exception as e:
                    print(f"Error processing object {obj}: {e}")
                    continue
            
            # Logout and close
            self.session.logout()
            self.session.closeSession()
            
        except Exception as e:
            print(f"Error listing keys: {e}")
        
        return keys
    
    def filter_keys(self, username: str, password: str, key_class: str = None, key_type: str = None, label: str = None, key_id: str = None) -> List[KeyInfo]:
        """Filter keys and return KeyInfo list"""
        keys = []
        
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return keys
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # Build filter template
            template = []
            
            if key_class:
                if key_class == "SECRET_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY))
                elif key_class == "PRIVATE_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY))
                elif key_class == "PUBLIC_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY))
            
            if key_type:
                if key_type == "AES":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES))
                elif key_type == "RSA":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA))
                elif key_type == "EC":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_EC))
            
            if label:
                template.append((PyKCS11.CKA_LABEL, label))
            
            if key_id:
                id_bytes = bytes.fromhex(key_id)
                template.append((PyKCS11.CKA_ID, id_bytes))
            
            # Find objects with template
            objects = self.session.findObjects(template)
            
            for obj in objects:
                try:
                    # Get object attributes
                    attrs = self.session.getAttributeValue(obj, [
                        PyKCS11.CKA_CLASS,
                        PyKCS11.CKA_KEY_TYPE,
                        PyKCS11.CKA_LABEL,
                        PyKCS11.CKA_ID
                    ])
                    
                    key_info = self._create_key_info(attrs)
                    if key_info:
                        keys.append(key_info)
                    
                except Exception as e:
                    print(f"Error processing object {obj}: {e}")
                    continue
            
            # Logout and close
            self.session.logout()
            self.session.closeSession()
            
        except Exception as e:
            print(f"Error filtering keys: {e}")
        
        return keys
    
    def find_key(self, username: str, password: str, key_class: str = None, key_type: str = None, label: str = None, key_id: str = None) -> Optional[KeyDetailResponse]:
        """Find specific key with detailed attributes"""
        
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return None
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # Build filter template
            template = []
            
            if key_class:
                if key_class == "SECRET_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY))
                elif key_class == "PRIVATE_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY))
                elif key_class == "PUBLIC_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY))
            
            if key_type:
                if key_type == "AES":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES))
                elif key_type == "RSA":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA))
                elif key_type == "EC":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_EC))
            
            if label:
                template.append((PyKCS11.CKA_LABEL, label))
            
            if key_id:
                id_bytes = bytes.fromhex(key_id)
                template.append((PyKCS11.CKA_ID, id_bytes))
            
            # Find objects with template
            objects = self.session.findObjects(template)
            
            if not objects:
                self.session.logout()
                self.session.closeSession()
                return None
            
            # Get first matching object
            obj = objects[0]
            
            # Get all attributes
            attrs = self.session.getAttributeValue(obj, [
                PyKCS11.CKA_CLASS,
                PyKCS11.CKA_KEY_TYPE,
                PyKCS11.CKA_LABEL,
                PyKCS11.CKA_ID,
                PyKCS11.CKA_TOKEN,
                PyKCS11.CKA_PRIVATE,
                PyKCS11.CKA_SENSITIVE,
                PyKCS11.CKA_EXTRACTABLE,
                PyKCS11.CKA_LOCAL,
                PyKCS11.CKA_MODIFIABLE,
                PyKCS11.CKA_DESTROYABLE
            ])
            
            # Map class and type
            key_class_str, key_type_str = self._map_class_and_type(attrs[0], attrs[1])
            
            # Process label and ID
            label_str = self._process_label(attrs[2])
            key_id_str = self._process_key_id(attrs[3])
            
            # Logout and close
            self.session.logout()
            self.session.closeSession()
            
            return KeyDetailResponse(
                key_class=key_class_str,
                key_type=key_type_str,
                label=label_str,
                key_id=key_id_str,
                token=bool(attrs[4]),
                private=bool(attrs[5]),
                sensitive=bool(attrs[6]),
                extractable=bool(attrs[7]),
                local=bool(attrs[8]),
                modifiable=bool(attrs[9]),
                destroyable=bool(attrs[10])
            )
            
        except Exception as e:
            print(f"Error finding key: {e}")
            return None
    
    def _create_key_info(self, attrs) -> Optional[KeyInfo]:
        """Helper to create KeyInfo from attributes"""
        try:
            key_class_str, key_type_str = self._map_class_and_type(attrs[0], attrs[1])
            label_str = self._process_label(attrs[2])
            key_id_str = self._process_key_id(attrs[3])
            
            return KeyInfo(
                key_class=key_class_str,
                key_type=key_type_str,
                label=label_str,
                key_id=key_id_str
            )
        except Exception as e:
            print(f"Error creating KeyInfo: {e}")
            return None
        
    def check_connection(self) -> bool:
        """Check if connection to CloudHSM is established"""
        session = None
        try: 
             # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return False
            
            # Open session
            session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)    
            return True
        
        except Exception as e:
            print(f"Error checking connection: {e}")
            return False
        finally:
            if session:
                session.closeSession()
    
    def _map_class_and_type(self, obj_class, key_type):
        """Helper to map PKCS11 constants to strings"""
        if obj_class == PyKCS11.CKO_SECRET_KEY:
            key_class_str = "SECRET_KEY"
        elif obj_class == PyKCS11.CKO_PRIVATE_KEY:
            key_class_str = "PRIVATE_KEY"
        elif obj_class == PyKCS11.CKO_PUBLIC_KEY:
            key_class_str = "PUBLIC_KEY"
        else:
            key_class_str = f"UNKNOWN_{obj_class}"
        
        if key_type == PyKCS11.CKK_AES:
            key_type_str = "AES"
        elif key_type == PyKCS11.CKK_RSA:
            key_type_str = "RSA"
        elif key_type == PyKCS11.CKK_EC:
            key_type_str = "EC"
        else:
            key_type_str = f"UNKNOWN_{key_type}"
        
        return key_class_str, key_type_str
    
    def _process_label(self, label):
        """Helper to process label attribute"""
        if not label:
            return None
        try:
            return bytes(label).decode('utf-8', errors='ignore')
        except:
            return str(label)
    
    def _process_key_id(self, key_id):
        """Helper to process key ID attribute"""
        if not key_id:
            return None
        try:
            return bytes(key_id).hex()
        except:
            return str(key_id)
    
    def logout(self):
        """Logout from CloudHSM session"""
        try:
            if self.session:
                self.session.logout()
                self.session.closeSession()
                self.session = None
        except Exception as e:
            print(f"Error during logout: {e}")
    
    def create_key(self, username: str, password: str, request: CreateKeyRequest) -> CreateKeyResponse:
        """Create a new key in CloudHSM"""
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return CreateKeyResponse(success=False, message="No HSM slots available")
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # Check if key with same label already exists
            existing_keys = self.session.findObjects([(PyKCS11.CKA_LABEL, request.label)])
            if existing_keys:
                self.session.logout()
                self.session.closeSession()
                return CreateKeyResponse(
                    success=False, 
                    message=f"KeyWithLabelAlreadyExists: A Key with label {request.label} already exists in HSM, for ease of access we recommend using unique label per key"
                )
            
            if request.key_class == "SECRET_KEY":
                self._create_secret_key(request)
            elif request.key_class == "PRIVATE_KEY" or request.key_class == "PUBLIC_KEY":
                self._create_key_pair(request)
            else:
                return CreateKeyResponse(success=False, message=f"Unsupported key class: {request.key_class}")
            
            # Logout and close
            self.session.logout()
            self.session.closeSession()
            
            return CreateKeyResponse(
                success=True,
                message=f"Key '{request.label}' created successfully"
            )
            
        except Exception as e:
            return CreateKeyResponse(success=False, message=f"Error creating key: {str(e)}")
    
    def _create_secret_key(self, request: CreateKeyRequest):
        """Create a secret key (AES)"""
        template = [
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY),
            (PyKCS11.CKA_LABEL, request.label),
            (PyKCS11.CKA_TOKEN, request.token),
            (PyKCS11.CKA_PRIVATE, request.private),
            (PyKCS11.CKA_SENSITIVE, request.sensitive),
            (PyKCS11.CKA_EXTRACTABLE, request.extractable),
        ]
        
        if request.key_type == "AES":
            template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES))
            key_size = request.key_size or 32  # Default 256-bit
            template.append((PyKCS11.CKA_VALUE_LEN, key_size))
            
            if request.encrypt is not None:
                template.append((PyKCS11.CKA_ENCRYPT, request.encrypt))
            if request.decrypt is not None:
                template.append((PyKCS11.CKA_DECRYPT, request.decrypt))
            
            mechanism = PyKCS11.Mechanism(PyKCS11.CKM_AES_KEY_GEN, None)
            self.session.generateKey(template, mecha=mechanism)
            return
        
        raise ValueError(f"Unsupported secret key type: {request.key_type}")
    
    def _create_key_pair(self, request: CreateKeyRequest):
        """Create a key pair (RSA/EC)"""
        if request.key_type == "RSA":
            key_size = request.key_size or 2048
            
            public_template = [
                (PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY),
                (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA),
                (PyKCS11.CKA_MODULUS_BITS, key_size),
                (PyKCS11.CKA_PUBLIC_EXPONENT, (0x01, 0x00, 0x01)),
                (PyKCS11.CKA_LABEL, f"{request.label}-public"),
                (PyKCS11.CKA_TOKEN, request.token),
            ]
            
            private_template = [
                (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
                (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA),
                (PyKCS11.CKA_LABEL, request.label),
                (PyKCS11.CKA_TOKEN, request.token),
                (PyKCS11.CKA_PRIVATE, request.private),
                (PyKCS11.CKA_SENSITIVE, request.sensitive),
                (PyKCS11.CKA_EXTRACTABLE, request.extractable),
            ]
            
            if request.encrypt is not None:
                public_template.append((PyKCS11.CKA_ENCRYPT, request.encrypt))
            if request.verify is not None:
                public_template.append((PyKCS11.CKA_VERIFY, request.verify))
            if request.decrypt is not None:
                private_template.append((PyKCS11.CKA_DECRYPT, request.decrypt))
            if request.sign is not None:
                private_template.append((PyKCS11.CKA_SIGN, request.sign))
            
            mechanism = PyKCS11.Mechanism(PyKCS11.CKM_RSA_PKCS_KEY_PAIR_GEN, None)
            self.session.generateKeyPair(
                public_template,
                private_template,
                mecha=mechanism
            )
            return
        
        raise ValueError(f"Unsupported key pair type: {request.key_type}")
    
    def delete_key(self, username: str, password: str, request: DeleteKeyRequest) -> DeleteKeyResponse:
        """Delete key(s) from CloudHSM"""
        try:
            # Initialize PKCS11
            self.pkcs11 = PyKCS11.PyKCS11Lib()
            self.pkcs11.load(self.pkcs11_lib)
            
            # Get slots
            slots = self.pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return DeleteKeyResponse(success=False, message="No HSM slots available")
            
            # Open session
            self.session = self.pkcs11.openSession(slots[0], PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
            
            # Login
            login_pin = f"{username}:{password}"
            self.session.login(login_pin)
            
            # Build filter template
            template = []
            
            if request.key_class:
                if request.key_class == "SECRET_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY))
                elif request.key_class == "PRIVATE_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY))
                elif request.key_class == "PUBLIC_KEY":
                    template.append((PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY))
            
            if request.key_type:
                if request.key_type == "AES":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES))
                elif request.key_type == "RSA":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA))
                elif request.key_type == "EC":
                    template.append((PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_EC))
            
            if request.label:
                template.append((PyKCS11.CKA_LABEL, request.label))
            
            if request.key_id:
                id_bytes = bytes.fromhex(request.key_id)
                template.append((PyKCS11.CKA_ID, id_bytes))
            
            # Find objects to delete
            objects = self.session.findObjects(template)
            
            if not objects:
                self.session.logout()
                self.session.closeSession()
                return DeleteKeyResponse(success=False, message="No matching keys found")
            
            # Delete all matching objects
            deleted_count = 0
            for obj in objects:
                try:
                    self.session.destroyObject(obj)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting object {obj}: {e}")
            
            # Logout and close
            self.session.logout()
            self.session.closeSession()
            
            return DeleteKeyResponse(
                success=True,
                message=f"Successfully deleted {deleted_count} key(s)",
                deleted_count=deleted_count
            )
            
        except Exception as e:
            return DeleteKeyResponse(success=False, message=f"Error deleting key: {str(e)}")
    
    def __del__(self):
        """Cleanup session on object destruction"""
        self.logout()