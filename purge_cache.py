#!/usr/bin/env python3
"""
Purge Cache Utility Script

This script provides a convenient way to clean up cached files
(uploads and outputs) from the command line or via Docker.

Usage:
    python purge_cache.py
    
    OR via Docker:
    docker exec vulnerability-reporter python purge_cache.py
"""

import shutil
import sys
from pathlib import Path


def get_directory_size(directory: Path) -> tuple[int, int]:
    """
    Calculate total size and file count of a directory.
    
    Args:
        directory: Path to directory
        
    Returns:
        Tuple of (file_count, total_size_bytes)
    """
    if not directory.exists():
        return 0, 0
    
    file_count = 0
    total_size = 0
    
    for item in directory.rglob("*"):
        if item.is_file():
            file_count += 1
            total_size += item.stat().st_size
    
    return file_count, total_size


def format_size(size_bytes: int) -> str:
    """
    Format size in bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def purge_directory(directory: Path, name: str) -> tuple[int, int]:
    """
    Purge all files from a directory.
    
    Args:
        directory: Path to directory to purge
        name: Name of directory (for logging)
        
    Returns:
        Tuple of (files_deleted, bytes_deleted)
    """
    if not directory.exists():
        print(f"⚠️  {name} directory does not exist: {directory}")
        return 0, 0
    
    files_deleted = 0
    bytes_deleted = 0
    
    for item in directory.iterdir():
        try:
            if item.is_file():
                size = item.stat().st_size
                item.unlink()
                files_deleted += 1
                bytes_deleted += size
                print(f"  ✓ Deleted file: {item.name}")
            elif item.is_dir():
                # Get size before deleting
                dir_files, dir_size = get_directory_size(item)
                shutil.rmtree(item)
                files_deleted += dir_files
                bytes_deleted += dir_size
                print(f"  ✓ Deleted directory: {item.name} ({dir_files} files, {format_size(dir_size)})")
        except Exception as e:
            print(f"  ✗ Failed to delete {item.name}: {e}")
    
    return files_deleted, bytes_deleted


def main():
    """Main function to purge cache."""
    print("=" * 70)
    print("🗑️  CACHE PURGE UTILITY")
    print("=" * 70)
    print()
    
    # Define directories
    uploads_dir = Path("/app/uploads")
    output_dir = Path("/app/output")
    
    # Check if running inside Docker
    if not uploads_dir.exists() and not output_dir.exists():
        # Try current directory structure
        uploads_dir = Path("uploads")
        output_dir = Path("output")
    
    # Get current cache info
    print("📊 Current Cache Status:")
    print("-" * 70)
    
    uploads_files, uploads_size = get_directory_size(uploads_dir)
    output_files, output_size = get_directory_size(output_dir)
    total_files = uploads_files + output_files
    total_size = uploads_size + output_size
    
    print(f"Uploads:  {uploads_files:>4} files  |  {format_size(uploads_size):>10}")
    print(f"Outputs:  {output_files:>4} files  |  {format_size(output_size):>10}")
    print(f"{'─' * 70}")
    print(f"Total:    {total_files:>4} files  |  {format_size(total_size):>10}")
    print()
    
    if total_files == 0:
        print("✨ Cache is already clean! Nothing to purge.")
        return
    
    # Confirm deletion
    print("⚠️  WARNING: This will permanently delete all cached files!")
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Purge cancelled.")
        return
    
    print()
    print("🧹 Purging cache...")
    print("-" * 70)
    
    # Purge uploads directory
    print()
    print("📁 Cleaning uploads directory...")
    uploads_deleted_files, uploads_deleted_size = purge_directory(uploads_dir, "Uploads")
    
    # Purge output directory
    print()
    print("📁 Cleaning output directory...")
    output_deleted_files, output_deleted_size = purge_directory(output_dir, "Output")
    
    # Summary
    total_deleted_files = uploads_deleted_files + output_deleted_files
    total_deleted_size = uploads_deleted_size + output_deleted_size
    
    print()
    print("=" * 70)
    print("✅ PURGE COMPLETE")
    print("=" * 70)
    print(f"Files deleted:  {total_deleted_files}")
    print(f"Space freed:    {format_size(total_deleted_size)}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Purge cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
