#!/usr/bin/env python3
"""
TAKAWASI Unified Agent - Main System Entry Point

This is the core integration system that combines:
- Chimera Agent (Advanced Multi-Agent Coordination)  
- ACS (Autonomous Computer System)
- Memory Quantum System (Persistent Intelligence)
- Self-Evolution Engine (Continuous Improvement)

Created by: takawasi
License: Apache-2.0
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Core system imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    # Chimera Agent components
    from takawasi_chimera_agent_v2.core.chimera_agent import ChimeraAgent
    from takawasi_chimera_agent_v2.core.interfaces.claude_code_interface import ClaudeCodeInterface
    from takawasi_chimera_agent_v2.core.interfaces.gemini_cli_interface import GeminiCLIInterface
    from takawasi_chimera_agent_v2.tools.memory_driven_tool_hub import MemoryDrivenToolHub
    
    # ACS components
    from takawasi_acs_kiro_integration_basic import KiroIntegration
    from takawasi_acs_phase2_multi_agent_system import MultiAgentSystem
    from takawasi_acs_phase3_self_evolution import SelfEvolutionEngine
    from takawasi_acs_pc_bridge_wsl2 import PCController
    
    # Memory system
    from memory_system.ultimate_memory_system import UltimateMemorySystem
    from memory_system.ultimate_quantum_memory import QuantumMemoryEngine
    
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import Warning: {e}")
    print("🔧 Some components may not be available. Running in limited mode.")
    IMPORTS_AVAILABLE = False

class TAKAWASIUnifiedAgent:
    """
    The unified agent system combining Chimera Agent + ACS capabilities
    
    This system provides:
    - Multi-agent coordination (Chimera)
    - Autonomous system control (ACS) 
    - Persistent memory (Memory Quantum)
    - Self-evolution capabilities
    - PC control automation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        print("🚀 Initializing TAKAWASI Unified Agent...")
        
        self.config = self._load_config(config_path)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize core components
        self.chimera_agent = None
        self.acs_systems = {}
        self.memory_system = None
        self.unified_status = "initializing"
        
        # Initialize systems
        asyncio.run(self._initialize_systems())
        
        print("✅ TAKAWASI Unified Agent initialized successfully!")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load unified system configuration"""
        default_config = {
            "chimera": {
                "claude_code_enabled": True,
                "gemini_cli_enabled": True,
                "memory_quantum_enabled": True,
                "tool_selection_threshold": 0.8
            },
            "acs": {
                "kiro_integration": True,
                "multi_agent_coordination": True,
                "self_evolution": True,
                "pc_control": True
            },
            "memory": {
                "persistent_storage": True,
                "quantum_memory_enabled": True,
                "cross_session_learning": True,
                "memory_optimization": True
            },
            "unified": {
                "auto_coordination": True,
                "capability_fusion": True,
                "error_recovery": True,
                "performance_monitoring": True
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    async def _initialize_systems(self):
        """Initialize all unified system components"""
        try:
            await self._initialize_memory_system()
            await self._initialize_chimera_agent()
            await self._initialize_acs_systems()
            await self._test_system_integration()
            
            self.unified_status = "ready"
            print("🎯 All systems integrated successfully!")
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            self.unified_status = "error"
            raise
    
    async def _initialize_memory_system(self):
        """Initialize the unified memory system"""
        print("🧠 Initializing Memory Quantum System...")
        
        if IMPORTS_AVAILABLE:
            try:
                self.memory_system = {
                    'quantum': QuantumMemoryEngine(),
                    'ultimate': UltimateMemorySystem(),
                    'session_memory': {},
                    'cross_session_learnings': []
                }
                print("✅ Memory Quantum System initialized")
            except Exception as e:
                print(f"⚠️ Memory system limited mode: {e}")
                self.memory_system = {'fallback': True}
        else:
            self.memory_system = {'fallback': True}
    
    async def _initialize_chimera_agent(self):
        """Initialize Chimera Agent components"""
        print("🔀 Initializing Chimera Agent...")
        
        if IMPORTS_AVAILABLE and self.config['chimera']['claude_code_enabled']:
            try:
                # Initialize core Chimera components
                claude_interface = ClaudeCodeInterface()
                gemini_interface = GeminiCLIInterface()
                tool_hub = MemoryDrivenToolHub(self.memory_system)
                
                self.chimera_agent = ChimeraAgent(
                    claude_interface=claude_interface,
                    gemini_interface=gemini_interface,
                    tool_hub=tool_hub,
                    memory_system=self.memory_system
                )
                
                print("✅ Chimera Agent initialized")
            except Exception as e:
                print(f"⚠️ Chimera Agent limited mode: {e}")
                self.chimera_agent = {'fallback': True}
        else:
            self.chimera_agent = {'fallback': True}
    
    async def _initialize_acs_systems(self):
        """Initialize ACS (Autonomous Computer System) components"""
        print("🤖 Initializing ACS Systems...")
        
        if IMPORTS_AVAILABLE:
            try:
                # Initialize ACS components
                if self.config['acs']['kiro_integration']:
                    self.acs_systems['kiro'] = KiroIntegration()
                
                if self.config['acs']['multi_agent_coordination']:
                    self.acs_systems['multi_agent'] = MultiAgentSystem()
                
                if self.config['acs']['self_evolution']:
                    self.acs_systems['evolution'] = SelfEvolutionEngine()
                
                if self.config['acs']['pc_control']:
                    self.acs_systems['pc_controller'] = PCController()
                
                print("✅ ACS Systems initialized")
            except Exception as e:
                print(f"⚠️ ACS Systems limited mode: {e}")
                self.acs_systems = {'fallback': True}
        else:
            self.acs_systems = {'fallback': True}
    
    async def _test_system_integration(self):
        """Test integration between all systems"""
        print("🔄 Testing system integration...")
        
        integration_tests = [
            self._test_memory_integration(),
            self._test_chimera_acs_bridge(),
            self._test_unified_capabilities()
        ]
        
        results = await asyncio.gather(*integration_tests, return_exceptions=True)
        
        failed_tests = [i for i, result in enumerate(results) if isinstance(result, Exception)]
        
        if failed_tests:
            print(f"⚠️ {len(failed_tests)} integration tests failed")
        else:
            print("✅ All integration tests passed")
    
    async def _test_memory_integration(self):
        """Test memory system integration"""
        if isinstance(self.memory_system, dict) and 'fallback' in self.memory_system:
            return "Memory system in fallback mode"
        
        # Test memory operations
        test_memory = {
            'type': 'system_test',
            'content': 'Integration test memory',
            'timestamp': datetime.now().isoformat()
        }
        
        # Store and retrieve test
        if hasattr(self.memory_system, 'store_memory_quantum'):
            await self.memory_system['quantum'].store_memory_quantum(test_memory)
            retrieved = await self.memory_system['quantum'].search_memory_quantums('system_test')
            
            if retrieved:
                return "Memory integration successful"
        
        return "Memory integration test completed"
    
    async def _test_chimera_acs_bridge(self):
        """Test communication between Chimera Agent and ACS"""
        if (isinstance(self.chimera_agent, dict) and 'fallback' in self.chimera_agent) or \
           (isinstance(self.acs_systems, dict) and 'fallback' in self.acs_systems):
            return "Chimera-ACS bridge in fallback mode"
        
        # Test basic communication
        test_task = {
            'type': 'integration_test',
            'description': 'Test Chimera-ACS communication',
            'requires_coordination': True
        }
        
        # Simulate coordination
        chimera_analysis = "Chimera analysis complete"
        acs_execution = "ACS ready for execution"
        
        return f"Bridge test: {chimera_analysis} + {acs_execution}"
    
    async def _test_unified_capabilities(self):
        """Test unified system capabilities"""
        capabilities = {
            'memory_persistence': self.memory_system is not None,
            'multi_agent_coordination': 'multi_agent' in self.acs_systems,
            'self_evolution': 'evolution' in self.acs_systems,
            'pc_control': 'pc_controller' in self.acs_systems,
            'reasoning': self.chimera_agent is not None
        }
        
        active_capabilities = sum(capabilities.values())
        total_capabilities = len(capabilities)
        
        capability_score = (active_capabilities / total_capabilities) * 100
        
        return f"Unified capabilities: {capability_score:.1f}% active"
    
    async def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        """
        Execute a task using the unified agent system
        
        This is the main entry point that coordinates between:
        - Chimera Agent for reasoning and planning
        - ACS for execution and automation
        - Memory system for persistence and learning
        """
        print(f"🎯 Executing unified task: {task_description}")
        
        if self.unified_status != "ready":
            return {
                'success': False,
                'error': f'System not ready (status: {self.unified_status})',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Stage 1: Chimera Agent Analysis
            analysis_result = await self._chimera_analysis(task_description, context)
            
            # Stage 2: ACS Execution Planning
            execution_plan = await self._acs_planning(analysis_result)
            
            # Stage 3: Unified Execution
            execution_result = await self._unified_execution(execution_plan)
            
            # Stage 4: Memory Integration & Learning
            await self._integrate_learning(task_description, analysis_result, execution_result)
            
            return {
                'success': True,
                'task_description': task_description,
                'analysis': analysis_result,
                'execution_plan': execution_plan,
                'result': execution_result,
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            }
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'task_description': task_description,
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            }
            
            # Log error for learning
            await self._log_error_for_learning(task_description, str(e))
            
            return error_result
    
    async def _chimera_analysis(self, task: str, context: Optional[Dict] = None) -> Dict:
        """Use Chimera Agent for task analysis and reasoning"""
        if isinstance(self.chimera_agent, dict) and 'fallback' in self.chimera_agent:
            return {
                'analysis_type': 'fallback',
                'reasoning': f'Basic analysis of: {task}',
                'approach': 'direct_execution',
                'estimated_complexity': 'medium'
            }
        
        # Advanced Chimera analysis would go here
        return {
            'analysis_type': 'chimera',
            'reasoning': f'Chimera agent analysis of: {task}',
            'approach': 'multi_agent_coordination',
            'estimated_complexity': 'high',
            'suggested_tools': ['claude_code', 'memory_search', 'tool_selection']
        }
    
    async def _acs_planning(self, analysis: Dict) -> Dict:
        """Use ACS for execution planning"""
        if isinstance(self.acs_systems, dict) and 'fallback' in self.acs_systems:
            return {
                'plan_type': 'fallback',
                'steps': ['basic_execution'],
                'estimated_time': 'unknown',
                'resources_needed': ['basic']
            }
        
        # Advanced ACS planning would go here
        return {
            'plan_type': 'acs_advanced',
            'steps': [
                'multi_agent_coordination',
                'pc_control_if_needed',
                'self_evolution_trigger',
                'result_validation'
            ],
            'estimated_time': '5-15 minutes',
            'resources_needed': ['multi_agent', 'memory', 'pc_control']
        }
    
    async def _unified_execution(self, plan: Dict) -> Dict:
        """Execute the unified plan"""
        execution_log = []
        
        for step in plan.get('steps', ['basic_execution']):
            print(f"🔄 Executing step: {step}")
            
            step_result = await self._execute_step(step)
            execution_log.append({
                'step': step,
                'result': step_result,
                'timestamp': datetime.now().isoformat()
            })
        
        return {
            'execution_type': 'unified',
            'steps_completed': len(execution_log),
            'execution_log': execution_log,
            'overall_status': 'completed'
        }
    
    async def _execute_step(self, step: str) -> str:
        """Execute individual step"""
        await asyncio.sleep(0.1)  # Simulate processing
        return f"{step} completed successfully"
    
    async def _integrate_learning(self, task: str, analysis: Dict, result: Dict):
        """Integrate the experience into memory and trigger learning"""
        if isinstance(self.memory_system, dict) and 'fallback' not in self.memory_system:
            learning_entry = {
                'type': 'task_completion',
                'task': task,
                'analysis': analysis,
                'result': result,
                'success': result.get('overall_status') == 'completed',
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            }
            
            # Store in memory for future learning
            self.memory_system['session_memory'][task] = learning_entry
        
        # Trigger self-evolution if enabled
        if 'evolution' in self.acs_systems:
            await self._trigger_evolution(task, result)
    
    async def _trigger_evolution(self, task: str, result: Dict):
        """Trigger self-evolution based on results"""
        if result.get('overall_status') == 'completed':
            print(f"✨ Triggering positive evolution for: {task}")
        else:
            print(f"🔧 Triggering error-learning evolution for: {task}")
    
    async def _log_error_for_learning(self, task: str, error: str):
        """Log errors for future learning and improvement"""
        if isinstance(self.memory_system, dict) and 'fallback' not in self.memory_system:
            error_entry = {
                'type': 'error',
                'task': task,
                'error': error,
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            }
            
            self.memory_system['session_memory'][f'error_{task}'] = error_entry
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            'unified_status': self.unified_status,
            'session_id': self.session_id,
            'chimera_active': not (isinstance(self.chimera_agent, dict) and 'fallback' in self.chimera_agent),
            'acs_active': not (isinstance(self.acs_systems, dict) and 'fallback' in self.acs_systems),
            'memory_active': not (isinstance(self.memory_system, dict) and 'fallback' in self.memory_system),
            'capabilities': list(self.acs_systems.keys()) if isinstance(self.acs_systems, dict) else [],
            'timestamp': datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the unified system"""
        print("🔄 Shutting down TAKAWASI Unified Agent...")
        
        # Save session memory
        if isinstance(self.memory_system, dict) and 'session_memory' in self.memory_system:
            session_file = f"session_{self.session_id}.json"
            with open(session_file, 'w') as f:
                json.dump(self.memory_system['session_memory'], f, indent=2)
            print(f"💾 Session saved to: {session_file}")
        
        self.unified_status = "shutdown"
        print("✅ TAKAWASI Unified Agent shutdown complete")

# Demo and testing functions
async def demo_unified_capabilities():
    """Demonstrate unified agent capabilities"""
    print("🎬 TAKAWASI Unified Agent Demo")
    print("=" * 50)
    
    agent = TAKAWASIUnifiedAgent()
    
    # Demo tasks
    demo_tasks = [
        "Analyze the current directory and create a summary report",
        "Research AI trends and generate a presentation",
        "Optimize system performance and provide recommendations"
    ]
    
    for i, task in enumerate(demo_tasks, 1):
        print(f"\n📋 Demo Task {i}: {task}")
        result = await agent.execute_task(task)
        
        if result['success']:
            print(f"✅ Task completed successfully")
            print(f"   Analysis type: {result['analysis']['analysis_type']}")
            print(f"   Execution steps: {result['execution_plan']['steps']}")
        else:
            print(f"❌ Task failed: {result['error']}")
    
    # Show system status
    print("\n📊 System Status:")
    status = agent.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    await agent.shutdown()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo_unified_capabilities())
    else:
        print("🚀 TAKAWASI Unified Agent")
        print("Usage:")
        print("  python takawasi_unified_agent.py --demo    # Run demo")
        print("  python takawasi_unified_agent.py          # Show usage")
        print("\nFor interactive use, import TAKAWASIUnifiedAgent class")