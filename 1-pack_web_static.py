def do_pack():
    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.mkdir("versions")

    # Get the current date and time
    now = datetime.now()

    # Create the archive name
    archive_name = "web_static_{}-{}-{}-{}-{}-{}".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )

    # Create the archive
    with tarfile.open(archive_name + ".tgz", "w:gz") as archive:
        for file in os.listdir("web_static"):
            archive.add("web_static/{}".format(file))

    # Return the archive path
    return archive_name + ".tgz"

