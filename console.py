#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex
from os import environ

classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_EOF(self, line):
        """Executes EOF command to exit the program"""
        return True

    def do_quit(self, line):
        """Executes quit command to exit the program"""
        return True

    def emptyline(self):
        """Handles emptyline"""
        pass

    def do_create(self, line):
        """Create a new instance of a class, saves it (to the JSON file)
        and prints the id.

        Args:
            line (str): class name
        """
        args = shlex.split(line)
        if len(args) < 1:
            print('** class name missing **')
            return

        if args[0] in classes:
            new_instance = classes[args[0]]()
            new_instance.save()
            print(new_instance.id)
        else:
            print('** class doesn\'t exist **')

    def do_show(self, line):
        """Prints the string representation of an instance based
        on the class name and id.

        Args:
            line (str): class name and id in the format <class name> <id>
        """
        args = shlex.split(line)
        if len(args) < 1:
            print('** class name missing **')
            return
        if args[0] not in classes:
            print('** class doesn\'t exist **')
            return
        if len(args) < 2:
            print('** instance id missing **')
            return
        key = args[0] + '.' + args[1]
        objs = storage.all()
        if key in objs:
            print(objs[key])
        else:
            print('** no instance found **')

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.

        Args:
            line (str): class name and id in the format <class name> <id>
        """
        args = shlex.split(line)
        if len(args) < 1:
            print('** class name missing **')
            return
        if args[0] not in classes:
            print('** class doesn\'t exist **')
            return
        if len(args) < 2:
            print('** instance id missing **')
            return
        key = args[0] + '.' + args[1]
        objs = storage.all()
        if key in objs:
            del objs[key]
            storage.save()
        else:
            print('** no instance found **')

    def do_all(self, line):
        """Prints all string representation of all instances based
        or not on the class name.

        Args:
            line (str): class name (optional)
        """
        args = shlex.split(line)
        objs = storage.all()
        if len(args) < 1:
            print([str(objs[key]) for key in objs])
        elif args[0] in classes:
            print([str(objs[key]) for key in objs if args[0] in key])
        else:
            print('** class doesn\'t exist **')

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).

        Args:
            line (str): class name, id, attribute name, and attribute value
        """
        args = shlex.split(line)
        if len(args) < 1:
            print('** class name missing **')
            return
        if args[0] not in classes:
            print('** class doesn\'t exist **')
            return
        if len(args) < 2:
            print('** instanceid missing **')
            return
        key = args[0] + '.' + args[1]
        objs = storage.all()
        if key not in objs:
            print('** no instance found **')
            return
        if len(args) < 3:
            print('** attribute name missing **')
            return
        if len(args) < 4:
            print('** value missing **')
            return
        instance = objs[key]
        attr_name = args[2]
        attr_value = args[3]

        # Check if the attribute is a numeric type and convert the value
        if attr_name in HBNBCommand.types:
            attr_value = HBNBCommand.types[attr_name](attr_value)

        setattr(instance, attr_name, attr_value)
        instance.save()

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        It evaluates the line as Python code and executes it.
        """
        args = line.split('.')
        if len(args) >= 2:
            cls_name = args[0]
            cmd = args[1].split('(')[0]
            if cls_name in classes and cmd in HBNBCommand.dot_cmds:
                _id = ''
                if '(' in line and ')' in line:
                    _id = line.split('(')[1].split(')')[0]
                if ',' in _id:
                    _id = _id.split(',')[0].strip(' "')
                if cmd == 'update' and '{' in line and '}' in line:
                    kwargs = line.split('{')[1].split('}')[0].split(',')
                    args = ['"' + _id + '"'] + kwargs
                else:
                    args = ['"' + _id + '"']
                if cmd == 'update' and args[1][0] != '{':
                    args.insert(2, '""')
                line = cmd + ' ' + cls_name + ' ' + ' '.join(args)
                self.onecmd(line)
                return
        super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

