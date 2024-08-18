# main.py
import os
import json
from datetime import datetime
import subprocess


class GitUtils:

    @staticmethod
    def get_tags():
        result = subprocess.run(['git', 'tag', '--sort=-creatordate'], stdout=subprocess.PIPE)
        tags = result.stdout.decode().splitlines()
        if len(tags) == 0:
            return None, None
        if len(tags) == 1:
            return tags[0], None
        return tags[0], tags[1]

    @staticmethod
    def get_commit_messages(tag1, tag2):
        if tag2:
            result = subprocess.run(['git', 'log', f'{tag2}..{tag1}', '--pretty=format:%s'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['git', 'log', tag1, '--pretty=format:%s'], stdout=subprocess.PIPE)
        return result.stdout.decode().splitlines()

    @staticmethod
    def get_initial_commit():
        result = subprocess.run(['git', 'rev-list', '--max-parents=0', 'HEAD'], stdout=subprocess.PIPE)
        return result.stdout.decode().strip()

class ChangelogGenerator:

    @staticmethod
    def create_changelog(tag, messages):
        header = f'### {tag}\n'
        changelog_content = ''.join([f'- {msg}\n' for msg in messages])
        
        # Read existing content
        try:
            with open('CHANGELOG.md', 'r') as f:
                existing_content = f.read()
        except FileNotFoundError:
            existing_content = ''
        
        # Write new content on top
        with open('CHANGELOG.md', 'w') as f:
            f.write(header + changelog_content + '\n' + existing_content)

    @staticmethod
    def create_txt_log(tag, messages):
        with open('changelog.txt', 'a') as f:
            f.write('---------------------------------------------------------------------------------------------------\n')
            f.write(f'Version: {tag}\n')
            f.write(f'Date: {datetime.now().strftime("%Y-%m-%d")}\n')
            f.write('  Changes:\n')
            for msg in messages:
                f.write(f'    - {msg}\n')
            f.write('\n')

    @staticmethod
    def update_info_json(tag):
        with open('info.json', 'r+') as f:
            data = json.load(f)
            data['version'] = tag
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


def main():
    current_tag, previous_tag = GitUtils.get_tags()

    if not previous_tag:
        previous_tag = GitUtils.get_initial_commit()

    commit_messages = GitUtils.get_commit_messages(current_tag, previous_tag)

    ChangelogGenerator.create_changelog(current_tag, commit_messages)
    ChangelogGenerator.create_txt_log(current_tag, commit_messages)
    ChangelogGenerator.update_info_json(current_tag)

if __name__ == '__main__':
    main()
