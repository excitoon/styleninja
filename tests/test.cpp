#include <asdasd>

namespace x
{

template <typename A>
class B
{
};

template <typename D> class M
{
};

class C: public A, B,
        protected C
{
    int b;
    int c;

private:
    int a;
    class Sub
    {
        int b;
        enum class E
        {
            Val1,
            Val2,
            Val3
        };

    protected:
        int f();
    };

    void f(int a,
            int b,
            int c)
    {
    }

    void long_function_name(
            int b,
            int c)
    {
    bad_indent;
        b = 2 >> c;
    }
}

}

int main()
{
    char c = '{';
    int a = 1 << 2;
    std::string s = "{";
    std::string s2 = u8R"COO({{{{"{{{{)COO";

    for (size_t i = 0; i < 10; ++i)
    {
        std::cout << "hi";
    }

    std::cout << "A"
        << "B"
        << "C";

    if (j > 0)
        if (i > 0)
            std::cout << "a"
                << "b"
                << "\n";

    std::copy(a.begin(),
            a.end(), std::advance(
                a+b+c+d));

    if (a < 0)
        if (1)
            for (int a = 0; i < 1; ++i)
            {
                {
                    std::cout << a
                        << b+c
                        << "\n";
                }
            }
    a = 1;

    std::cout << a << b << c
        << func(
            a, b, c)
        << fun2(a, b,
            c) << "\n";

    func(func(func(
            arg1, arg2, arg3, func(
                arg1))));

    auto x = []()
    {
        something();
    };

    auto xx([]()
            {
                something();
            });

    switch(a)
    {
        case 0:
            a << aaaa
                << vvv
                << ccc;
            break;

        case -1:
            if (asdasd)
                for (a,b,c)
                    a << sss
                        << ddd
                        << bbb;
            break;

        case 1:
            func();
            func2();
            func3();
            break;

        case 2:
            {
                func2();
                func3();
                func4();
                a = b;
                b = c;
                c = 1;
                break;
            }

        default:
            break;
    }

    return 0;
}
