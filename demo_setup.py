#!/usr/bin/env python3
"""
TAKAWASI Unified Agent - Demo Setup Script

This script creates the necessary demo database files for the unified system
to demonstrate functionality without requiring prior setup.

Created by: takawasi
License: Apache-2.0
"""

import asyncio
from pathlib import Path
from memory_quantum_core import MemoryQuantumCore
from acs_core import ACSCore
from chimera_core import ChimeraAgent

async def create_demo_databases():
    """Create demo database files with sample data"""
    print("🚀 TAKAWASI Unified Agent - Demo Setup")
    print("=" * 50)
    
    # Create Memory Quantum demo database
    print("🧠 Creating Memory Quantum demo database...")
    memory = MemoryQuantumCore("demo_memory_quantum.db")
    
    # Add sample memory quantums
    sample_memories = [
        ("System initialized successfully", "system_status", ["system", "init", "success"]),
        ("Task execution completed with 95% success rate", "task_result", ["execution", "success", "performance"]),
        ("Multi-agent coordination established", "coordination", ["agents", "cooperation", "network"]),
        ("Self-evolution cycle triggered", "evolution", ["learning", "improvement", "adaptation"])
    ]
    
    for content, content_type, tags in sample_memories:
        quantum_id = await memory.store_memory_quantum(content, content_type, tags)
        print(f"  💾 Stored: {quantum_id}")
    
    print("✅ Memory Quantum demo database created")
    
    # Create ACS demo database
    print("🤖 Creating ACS demo database...")
    acs_config = {
        'target_actions_per_second': 654.9,
        'kiro_integration': True,
        'multi_agent_coordination': True,
        'self_evolution': True,
        'pc_control': True
    }
    
    acs = ACSCore(acs_config)
    
    # Execute a demo task to populate the database
    demo_result = await acs.execute_task("Demo system initialization", "setup", 8)
    print(f"  ⚡ Demo task completed: {demo_result['success']}")
    
    # Copy to demo filename
    import shutil
    import glob
    acs_files = glob.glob('acs_core_*.db')
    if acs_files:
        shutil.copy(acs_files[0], 'demo_acs_core.db')
    print("✅ ACS demo database created")
    
    # Create Chimera demo session
    print("🔀 Creating Chimera demo data...")
    chimera = ChimeraAgent()
    
    demo_result = await chimera.execute_task("Initialize demo multi-agent system")
    print(f"  🤖 Chimera demo completed: {demo_result['success']}")
    
    # Copy performance data
    import glob
    perf_files = glob.glob('chimera_performance_*.json')
    if perf_files:
        shutil.copy(perf_files[0], 'demo_chimera_performance.json')
    print("✅ Chimera demo data created")
    
    print("\n🎯 Demo setup complete!")
    print("All demo databases are ready for unified system testing.")
    
    await memory.shutdown()
    await acs.shutdown()
    await chimera.shutdown()

def setup_demo_environment():
    """Setup demo environment synchronously"""
    print("🔧 Setting up demo environment...")
    
    # Ensure demo files exist
    demo_files = {
        'demo_memory_quantum.db': 'Memory Quantum database',
        'demo_acs_core.db': 'ACS Core database', 
        'demo_chimera_performance.json': 'Chimera performance data'
    }
    
    missing_files = []
    for filename, description in demo_files.items():
        if not Path(filename).exists():
            missing_files.append((filename, description))
    
    if missing_files:
        print(f"⚠️  Missing demo files: {len(missing_files)}")
        for filename, desc in missing_files:
            print(f"   - {filename}: {desc}")
        print("Run: python3 demo_setup.py --create to generate them")
        return False
    else:
        print("✅ All demo files present")
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        asyncio.run(create_demo_databases())
    elif len(sys.argv) > 1 and sys.argv[1] == "--check":
        setup_demo_environment()
    else:
        print("🚀 TAKAWASI Unified Agent - Demo Setup")
        print()
        print("Usage:")
        print("  python3 demo_setup.py --create    Create demo databases")
        print("  python3 demo_setup.py --check     Check demo environment")
        print()
        print("Demo files:")
        print("  - demo_memory_quantum.db         Memory Quantum database")
        print("  - demo_acs_core.db               ACS Core database")
        print("  - demo_chimera_performance.json   Chimera performance data")