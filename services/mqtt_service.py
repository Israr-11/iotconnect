import paho.mqtt.client as mqtt
import json
from typing import Callable, Dict, Any
from config.database import get_db
from services.device_service import DeviceService
from services.device_log_service import DeviceLogService

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client()
        self.device_service = DeviceService()
        self.device_log_service = DeviceLogService()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def connect(self, broker_host: str = "localhost", broker_port: int = 1883):
        """Connect to MQTT broker"""
        self.client.connect(broker_host, broker_port, 60)
        self.client.loop_start()  # STARTING BACKGROUND THREAD FOR MQTT
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        print(f"Connected to MQTT broker with result code {rc}")
        # SUBSCRIBE TO DEVICE STATUS TOPICS
        client.subscribe("iotconnect/devices/+/status")
        
    def on_message(self, client, userdata, msg):
        """Callback when message received from MQTT broker"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            # EXTRACT DEVICE_UID FROM TOPIC (e.g., "iotconnect/devices/device123/status")
            topic_parts = topic.split('/')
            if len(topic_parts) >= 3 and topic_parts[0] == "iotconnect" and topic_parts[1] == "devices":
                device_uid = topic_parts[2]
                
                # HANDLE DEVICE STATUS UPDATE
                if topic_parts[-1] == "status":
                    self._handle_device_status(device_uid, payload)
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    def _handle_device_status(self, device_uid: str, payload: Dict[str, Any]):
        """Handle device status update from MQTT"""
        # GET DATABASE SESSION (IN ACTUAL IMPLEMENTATION, USE A SESSION FACTORY)
        db = next(get_db())
        try:
            # GET DEVICE BY UID
            device = self.device_service.get_device_by_uid(db, device_uid)
            if device:
                # UPDATE DEVICE STATUS IN DATABASE
                if "status" in payload:
                    device, _ = self.device_service.toggle_device_status(
                        db, device.id, payload["status"], None
                    )
                    print(f"Updated device {device_uid} status to {payload['status']}")
        finally:
            db.close()
    
    def publish_device_status(self, device_uid: str, status: bool):
        """Publish device status change to MQTT"""
        topic = f"iotconnect/devices/{device_uid}/status"
        payload = json.dumps({"status": status})
        self.client.publish(topic, payload)
        print(f"Published status update for device {device_uid}: {status}")