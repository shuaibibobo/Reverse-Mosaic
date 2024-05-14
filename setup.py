from setuptools import setup, find_packages

setup(
    name='RMSecAgent',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'RMSecAgent = ReverseMosaic.rms_sec_agent:run'
        ]
    },
    install_requires=[
        'llama-index-llms-huggingface',
        'llama-index-embeddings-huggingface',
        'scipy',
        'argparse',
        'rich',
        'setuptools',
        'huggingface_hub',
        'numpy',
        'accelerate>=0.16.0,<1',
        'pyyaml',
        'torch>=1.13.1',
        'bitsandbytes>=0.39.0',
        'transformers[torch]>=4.28.1',
        'pdfplumber',
        'llama-index-readers-file'
    ],
    author='James Stevenson',
    description='A multi-agent binary analysis toolkit'
)
