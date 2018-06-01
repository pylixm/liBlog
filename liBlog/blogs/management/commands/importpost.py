# -*- coding:utf-8 -*-
import os
import ast
import traceback
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.transaction import atomic
from liBlog.blogs.models import Post, Category, Tag


class Command(BaseCommand):
    help = 'Import post md file into db.'

    @atomic()
    def handle(self, *args, **options):
        self.stdout.write('Start import markdown file into database.')
        post_file_paths = self.get_posts(settings.POST_SOURCE_PATH)
        self.stdout.write('Find [%s] markdown files. ' % len(post_file_paths))
        for post_file_path in post_file_paths:
            self.stdout.write('Import markdown file [%s]' % post_file_path)
            post_content = self.parse(post_file_path)
            self.import_db(post_content)

        self.stdout.write('Successfully imported database.')

    def get_posts(self, path):
        post_file_paths = []
        try:
            for root, dirs, names in os.walk(path):
                for name in names:
                    if name.endswith('.md') or name.endswith('.markdown'):
                        post_file_paths.append(os.path.join(root, name))
        except Exception as err:
            raise CommandError(str(err))
        return post_file_paths

    def parse(self, file_path):
        ret = {
            'title': '',
            'category': '',
            'publish_time': '',
            'tags': [],
            'post_content': ''
        }
        del_lines = []
        with open(file_path, 'r') as file:
            post_content_lines = file.readlines()
            for line in post_content_lines:
                # line_index = post_content_lines.index(line)
                if line == '---\n':
                    del_lines.append(line)
                elif line.startswith('layout'):
                    del_lines.append(line)
                elif line.startswith('title'):
                    ret['title'] = line.split(':')[1].strip('\n').strip(' ')
                    del_lines.append(line)
                elif line.startswith('category'):
                    ret['category'] = line.split(':')[1].strip('\n').strip(' ')
                    del_lines.append(line)
                elif line.startswith('date :'):
                    date = line.strip('\n').split(':')
                    try:
                        ret['publish_time'] = datetime.datetime.strptime(
                            ':'.join(date[1:]).strip(' '), '%Y-%m-%d %H:%M:%S')
                    except Exception as err:
                        ret['publish_time'] = datetime.datetime.strptime(
                            ':'.join(date[1:]).strip(' '), '%Y-%m-%d')

                    del_lines.append(line)
                elif line.startswith('tags'):
                    tags_str = line.split(':')[1].strip('\n') \
                        .replace('[', '["').replace(']', '"]') \
                        .replace(',', '","').replace(' ', '')
                    ret['tags'] = ast.literal_eval(tags_str.strip(' '))
                    del_lines.append(line)

            # 删除header信息
            for line in del_lines:
                post_content_lines.remove(line)

            post_content = "".join(post_content_lines)
            ret['post_content'] = post_content.strip('\n')

        return ret

    def import_db(self, pay_loads={}):
        """
        :param pay_loads: {
            'title': '',
            'category': '',
            'publish_time': '',
            'tags': [],
            'post_content': ''
        }
        :return:
        """
        try:
            category = Category.objects.filter(
                name__icontains=pay_loads['category'],
                status=Category.PUBLISH).first()
            if not category:
                category = Category.objects.create(
                    name=pay_loads['category'],
                    status=Category.PUBLISH
                )
            post = Post.objects.filter(title=pay_loads['title']).first()
            if not post:
                post = Post.objects.create(
                    title=pay_loads['title'],
                    publish_time=pay_loads['publish_time'],
                    content=pay_loads['post_content'],
                    summary=pay_loads['post_content'][:200],
                    category=category,
                    status=Post.PUBLISH
                )
            else:
                post.content = pay_loads['post_content']
                post.summary = pay_loads['post_content'][:200]
                post.save()
            for tag_name in pay_loads['tags']:
                tag = Tag.objects.filter(name__icontains=tag_name).first()
                if not tag:
                    tag = Tag.objects.create(name=tag_name)

                post.tags.add(tag)
        except KeyError as err:
            raise CommandError('Markdown format error: %s' % str(err))
        except Exception as err:
            raise CommandError(str(traceback.format_exc()))
