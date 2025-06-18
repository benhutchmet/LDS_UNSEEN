#!/bin/bash
#SBATCH --job-name="submit_download_ERA5"
#SBATCH --time=80:00:00
#SBATCH --mem=10000M
#SBATCH --account=canari
#SBATCH --partition=standard
#SBATCH --qos=long
#SBATCH -o /home/users/benhutch/LDS_UNSEEN/logs/submit_download_ERA5-%A_%a.out
#SBATCH -e /home/users/benhutch/LDS_UNSEEN/logs/submit_download_ERA5-%A_%a.err

# Set up the usage message
usage="Usage: sbatch submit_download_ERA5_jasmin.bash <start_year> <end_year> <start_month> <end_month>"

# Check the number of CLI arguments
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo $usage
    exit 1
fi

# Load the jaspy module
module load jaspy

# Load my python environment
source activate bens-conda-env2

# Load the args
start_year=$1
end_year=$2
start_month=$3
end_month=$4

# Set up the process script
process_script="/home/users/benhutch/LDS_UNSEEN/download_data/download_ERA5_jasmin.py"

# Echo the args
echo "Start year: ${start_year}"
echo "End year: ${end_year}"
echo "Start month: ${start_month}"
echo "End month: ${end_month}"

# ensure that these are all ints
if ! [[ "$start_year" =~ ^[0-9]+$ ]] || ! [[ "$end_year" =~ ^[0-9]+$ ]] || ! [[ "$start_month" =~ ^[0-9]+$ ]] || ! [[ "$end_month" =~ ^[0-9]+$ ]]; then
    echo "All arguments must be integers."
    echo $usage
    exit 1
fi

# run the python script with the arguments
python ${process_script} \
    --start_year ${start_year} \
    --end_year ${end_year} \
    --start_month ${start_month} \
    --end_month ${end_month}

# End of file
echo "End of file"