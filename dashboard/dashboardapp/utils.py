import open3d as o3d

def process_pointcloud(file_path):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(file_path)
    
    # Downsample (example processing step)
    downsampled_pcd = pcd.voxel_down_sample(voxel_size=0.05)

    # Save the processed point cloud
    output_path = file_path.replace('.ply', '_processed.ply')
    o3d.io.write_point_cloud(output_path, downsampled_pcd)

    return output_path
